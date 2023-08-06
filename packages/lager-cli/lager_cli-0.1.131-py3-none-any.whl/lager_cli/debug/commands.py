"""
    lager.debug.commands

    Debug an elf file
"""
import click
from ..context import get_default_gateway
from ..debug.gdb import debug
from ..gateway.commands import _status


@click.group(name='debug')
def _debug():
    """
        Lager gateway commands
    """
    pass

@_debug.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--mcu', required=False, default=None, help='MCU to query', type=click.INT)
def status(ctx, gateway, mcu):
    _status(ctx, gateway, mcu)


@_debug.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--interpreter', '-i', required=False, default='default', help='Select a specific interpreter / user interface')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Print verbose debug info')
@click.option('--tty', required=False, help='Use TTY for input/output by the program being debugged.')
@click.option('--quiet', '--silent', '-q', is_flag=True, default=False, help='Do not print the introductory and copyright messages. These messages are also suppressed in batch mode.')
@click.option('--args', required=False, help='Arguments passed to debugger')
@click.option('--ignore-missing/--no-ignore-missing', is_flag=True, default=False, help='Ignore missing files')
@click.option('--cwd', default=None, type=click.Path(exists=True, file_okay=False, resolve_path=True), help='Set current working directory')
@click.option('--cache/--no-cache', default=True, is_flag=True, help='Use cached source if ELF file unchanged', show_default=True)
@click.option('--mcu', required=False, default=None, help='MCU to query', type=click.INT)
@click.argument('elf_file', type=click.Path())
def gdb(ctx, gateway, interpreter, verbose, tty, quiet, args, ignore_missing, cwd, cache, mcu, elf_file):
    """
        Debug a DUT using an ELF file
    """
    debug(ctx, gateway, interpreter, verbose, tty, quiet, args, ignore_missing, cwd, cache, mcu, elf_file)


@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to connect')
@click.option('--force', is_flag=True, default=False, help='Disconnect debugger before reconnecting. If not set, connect will fail if debugger is already connected. Cannot be used with --ignore-if-connected', show_default=True)
@click.option('--ignore-if-connected', is_flag=True, default=False, help='If debugger is already connected, skip connection attempt and exit with success. Cannot be used with --force', show_default=True)
def connect(ctx, dut, mcu, force, ignore_if_connected):
    if force and ignore_if_connected:
        click.secho('Cannot specify --force and --ignore-if-connected', fg='red')
        ctx.exit(1)

    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    resp = session.debug_connect(dut, mcu, force, ignore_if_connected).json()
    if resp.get('start') == 'ok':
        click.secho('Connected!', fg='green')
    elif resp.get('already_running') == 'ok':
        click.secho('Debugger already connected, ignoring', fg='green')

@_debug.command()
@click.pass_context
@click.option('--dut', required=False, help='ID of DUT')
@click.option('--mcu', required=False, help='MCU to disconnect')
def disconnect(ctx, dut, mcu):
    if dut is None:
        dut = get_default_gateway(ctx)
    session = ctx.obj.session
    session.debug_disconnect(dut, mcu).json()
    click.secho('Disconnected!', fg='green')
