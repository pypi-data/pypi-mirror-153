"""
    lager.erase.commands

    Commands for erasing a DUT
"""
import click
from ..context import get_default_gateway
from ..util import stream_output

def do_reset(session, gateway, halt, mcu=None):
    """
        Perform the DUT reset
    """
    return session.reset_dut(gateway, halt, mcu)

@click.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.option('--halt', is_flag=True, help='Halt the DUT after reset. Default: do not halt', default=False, show_default=True)
@click.option('--mcu', required=False, default=None, help='MCU to target', type=click.INT)
def reset(ctx, gateway, halt, mcu):
    """
        Reset the DUT. By default will not halt the DUT; use `lager reset --halt` to reset and halt.
    """
    if gateway is None:
        gateway = get_default_gateway(ctx)
    resp = do_reset(ctx.obj.session, gateway, halt, mcu)
    stream_output(resp)
