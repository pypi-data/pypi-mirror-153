"""
    lager.erase.commands

    Commands for erasing a DUT
"""
import click
from ..context import get_default_gateway
from ..paramtypes import MemoryAddressType
from ..util import stream_output

@click.command()
@click.pass_context
@click.option('--gateway', '--dut', required=False, help='ID of gateway to which DUT is connected')
@click.argument('start_addr', type=MemoryAddressType())
@click.argument('length', type=MemoryAddressType())
@click.option('--mcu', required=False, default=None, help='MCU to target', type=click.INT)
def erase(ctx, gateway, start_addr, length, mcu):
    """
        Erase DUT
    """
    if gateway is None:
        gateway = get_default_gateway(ctx)

    session = ctx.obj.session
    addresses = dict(start_addr=start_addr, length=length, mcu=mcu)
    resp = session.erase_dut(gateway, addresses=addresses)
    stream_output(resp)
