"""
    lager.factory.commands

    Factory commands
"""
import os
import ast
import asyncio
import re
import pathlib
import concurrent.futures
import webbrowser

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape
import websockets
import sanic
from sanic import Sanic
from sanic.response import html, json, file
from sanic.errorpages import HTMLRenderer, exception_response

from ..paramtypes import EnvVarType
from ..context import get_default_gateway
from ..python.commands import zip_dir, MAX_ZIP_SIZE
from ..util import SizeLimitExceeded
from .parser import parse_code, StepNotFound

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ASSET_PATH = os.path.join(DIR_PATH, 'site')

def load_steps(base, folder):
    try:
        with open(os.path.join(base, folder, 'main.py'), 'rb') as f:
            main_py = f.read()
    except FileNotFoundError:
        click.secho(f'main.py not found in {folder}', fg='red', err=True)
        raise

    nodes = ast.parse(main_py, 'main.py')
    return parse_code(nodes)

@click.group()
def factory():
    """
        Lager Factory commands
    """
    pass

async def home(request):
    config = request.app.config
    try:
        steps = load_steps(config['CWD'], config['FOLDER'])
    except SyntaxError as exc:
        template = request.app.ctx.jinja.get_template("badsyntax.html")
        _name, (filename, line, col, code) = exc.args
        return html(template.render(filename=filename, line=line, col=col, code=code), status=500)
    except StepNotFound as exc:
        template = request.app.ctx.jinja.get_template("missingstep.html")
        step = exc.args[0]
        return html(template.render(step=step), status=500)

    template = request.app.ctx.jinja.get_template("index.html")
    return html(template.render(steps=steps))

async def start(request):
    config = request.app.config
    ctx = config['CONTEXT']
    session = ctx.obj.session
    with concurrent.futures.ThreadPoolExecutor() as pool:
        resp = await asyncio.get_running_loop().run_in_executor(
            pool, session.start_dev_factory, config['GATEWAY_ID'])

    return json(resp.json())

async def stop(request):
    print(request.json)
    return json({})

async def pipe(src, dst):
    while True:
        msg = await src.recv()
        await dst.send(msg)

async def websocket_handler(request, browser_ws, session_id):
    config = request.app.config
    ctx = config['CONTEXT']
    (uri, kwargs) = ctx.obj.websocket_connection_params(socktype='job', job_id=session_id)
    sock_kwargs = {}
    if kwargs.get('ssl_context'):
        sock_kwargs['ssl'] = kwargs['ssl_context']

    sock_kwargs['extra_headers'] = {k.decode(): v.decode() for (k, v) in kwargs['extra_headers']}
    async with websockets.connect(uri, **sock_kwargs) as server_ws:
        pipe1 = pipe(browser_ws, server_ws)
        pipe2 = pipe(server_ws, browser_ws)
        await asyncio.gather(pipe1, pipe2)

async def runner(request, session_id):
    config = request.app.config
    ctx = config['CONTEXT']
    session = ctx.obj.session
    gateway = config['GATEWAY_ID']

    secrets = config['SECRETS']

    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', gateway)
    post_data = [
        ('stdout_is_stderr', '0'),
        ('detach', '1'),
        ('env', f'LAGER_SESSION_ID={session_id}'),
        ('env', f'LAGER_GATEWAY_ID={gateway}'),
        ('env', f'LAGER_GATEWAY_NAME={clean_name}'),
        ('image', ''),
    ]
    for secret in secrets:
        name, value = secret.split('=', 1)
        if name.isidentifier():
            post_data.append(
                ('env', f'LAGER_SECRET_{name}={value}'),
            )

    cwd = config['CWD']
    folder = config['FOLDER']
    runnable = os.path.join(cwd, folder)
    try:
        max_content_size = 20_000_000
        zipped_folder = zip_dir(runnable, max_content_size=max_content_size)
    except SizeLimitExceeded:
        click.secho(f'Folder content exceeds max size of {max_content_size:,} bytes', err=True, fg='red')
        raise

    if len(zipped_folder) > MAX_ZIP_SIZE:
        click.secho(f'Zipped module content exceeds max size of {MAX_ZIP_SIZE:,} bytes', err=True, fg='red')
        raise SizeLimitExceeded()

    post_data.append(('module', zipped_folder))
    with concurrent.futures.ThreadPoolExecutor() as pool:
        _ = await asyncio.get_running_loop().run_in_executor(
            pool, session.run_python, gateway, post_data)

    return json({'ok': True})

async def after_start(app, loop, **kwargs):
    port = app.config['PORT']
    url = f'http://localhost:{port}'
    print(f'Factory App listening on {url}')
    try:
        webbrowser.get()
    except webbrowser.Error:
        return

    with concurrent.futures.ThreadPoolExecutor() as pool:
        await asyncio.get_running_loop().run_in_executor(
            pool, webbrowser.open_new, url)


async def image(request):
    src = request.args['src'][0]
    config = request.app.config
    cwd = pathlib.Path(config['CWD'])
    full_path = (cwd / src).resolve()
    if cwd not in full_path.parents:
        raise sanic.exceptions.NotFound()

    return await file(full_path)

@factory.command()
@click.pass_context
@click.option('--gateway', required=False, help='ID of gateway to which DUT is connected')
@click.option('--folder', type=click.Path(exists=True, file_okay=False, resolve_path=True), required=True, help='Path')
@click.option('--port', type=click.INT, required=False, default=8000, help='local listen port')
@click.option(
    '--secret',
    multiple=True, type=EnvVarType(), help='Secrets to set for the python script. '
    'Format is `--secret FOO=BAR` - this will set a secret named `FOO` to the value `BAR`')

def dev(ctx, gateway, folder, port, secret):
    """
        Test a factory instance locally
    """
    if gateway is None:
        gateway = get_default_gateway(ctx)

    cwd = os.getcwd()

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "sanic.root": {"level": "FATAL", "propagate": True},
            "sanic.error": {"level": "FATAL", "propagate": True},
        },
    }

    app = Sanic("Lager-Factory", log_config=log_config)
    app.config['CONTEXT'] = ctx
    app.config['GATEWAY_ID'] = gateway
    app.config['CWD'] = cwd
    app.config['FOLDER'] = folder
    app.config['PORT'] = port
    app.config['SECRETS'] = secret

    app.add_route(home, '/')
    app.add_route(start, '/factory/start', methods=['POST'])
    app.add_route(stop, '/factory/stop', methods=['POST'])
    app.add_route(runner, '/factory/run-station/new-runner/<session_id:uuid>', methods=['POST'])
    app.add_route(image, '/factory/run-station/img')
    app.add_websocket_route(websocket_handler, '/ws/job/<session_id:uuid>')
    app.static('/static', ASSET_PATH)

    app.signal('server.init.after')(after_start)

    env = Environment(
        loader=FileSystemLoader(ASSET_PATH),
        autoescape=select_autoescape()
    )
    app.ctx.jinja = env
    dev_mode = 'LAGER_SANIC_DEV' in os.environ
    app.run(port=port, motd=False, verbosity=0, dev=dev_mode, access_log=False)
