"""
    lager.lister.commands

    List commands
"""
import click
from ..context import get_default_gateway
from texttable import Texttable

def channel_num(mux, mapping):
    point = mux['scope_points'][0][1]
    if mux['role'] == 'analog':
        return ord(point) - ord('A') + 1
    if mux['role'] == 'logic':
        return int(point) + 1
    try:
        numeric = int(point, 10)
        return numeric
    except ValueError:
        return ord(point) - ord('A') + 1

def get_nets(ctx, gateway):
    session = ctx.obj.session
    resp = session.all_muxes(gateway)
    resp.raise_for_status()
    return resp.json()['muxes']


def display_nets(muxes, netname):
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(['l', 'r', 'r'])
    table.add_row(['name', 'type', 'channel'])
    for mux in muxes:
        for mapping in mux['mappings']:
            if netname is None or netname == mapping['net']:
                channel = channel_num(mux, mapping)
                table.add_row([mapping['net'], mux['role'], channel])

    click.echo(table.draw())

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
def net(ctx, gateway):
    """
        Lager net commands
    """
    if ctx.invoked_subcommand is not None:
        return

    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)

    display_nets(muxes, None)

def validate_net(ctx, muxes, netname, role):
    for mux in muxes:
        if mux['role'] != role:
            continue
        for mapping in mux['mappings']:
            if mapping['net'] == netname:
                return mapping
    raise click.UsageError(f'{role.title()} net with name `{netname}` not found!', ctx=ctx)

@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.argument('NETNAME')
def show(ctx, gateway, netname):
    """
        Show the available nets which match a given name
    """
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    display_nets(muxes, netname)

@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--voltdiv', help='Voltage division')
@click.option('--timediv', help='Time division')
@click.option('--voltoffset', help='Voltage offset')
@click.option('--timeoffset', help='Time offset')
@click.argument('NETNAME')
def trace(ctx, gateway, voltdiv, timediv, voltoffset, timeoffset, netname):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'analog')
    print('trace', dut_net)

@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--level', help='Voltage level')
@click.option('--slope', help='Time division')
@click.option('--mode', help='Voltage offset')
@click.argument('NETNAME')
@click.argument('TRIGGERTYPE')
def trigger(ctx, gateway, level, slope, mode, netname, triggertype):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'analog')

    print('trigger')

@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--vavg', is_flag=True, default=False, help='Average voltage')
@click.option('--freq', is_flag=True, default=False, help='Frequency')
@click.argument('NETNAME')
def measure(ctx, gateway, vavg, freq, netname):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'analog')

    print('measure')


@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--set-a')
@click.option('--set-b')
@click.option('--set-ax')
@click.option('--set-bx')
@click.option('--set-ay')
@click.option('--set-by')
@click.option('--move-a')
@click.option('--move-b')
@click.option('--move-ax')
@click.option('--move-bx')
@click.option('--move-ay')
@click.option('--move-by')
@click.option('--a-values', is_flag=True, default=False)
@click.option('--b-values', is_flag=True, default=False)
@click.argument('NETNAME')
def cursor(ctx, gateway, set_a, set_b, set_ax, set_bx, set_ay, set_by, move_a, move_b, move_ax, move_bx, move_ay, move_by, a_values, b_values, netname):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'analog')

    print('cursor')


@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--soc')
@click.option('--full')
@click.option('--empty')
@click.option('--curr-limit')
@click.option('--capacity')
@click.argument('NETNAME')
def battery(ctx, gateway, soc, full, empty, curr_limit, capacity, netname):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'battery')

    print('battery')

@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--max-settings', is_flag=True, default=False)
@click.option('--voltage')
@click.option('--current')
@click.argument('NETNAME')
def supply(ctx, gateway, max_settings, voltage, current, netname):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'power-supply')

    print('supply')


@net.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--max-settings', is_flag=True, default=False)
@click.option('--voltage')
@click.option('--resistance')
@click.option('--current')
@click.option('--power')
@click.argument('NETNAME')
def eload(ctx, gateway, max_settings, voltage, resistance, current, power, netname):
    if gateway is None:
        gateway = get_default_gateway(ctx)

    muxes = get_nets(ctx, gateway)
    dut_net = validate_net(ctx, muxes, netname, 'e-load')

    print('eload')
