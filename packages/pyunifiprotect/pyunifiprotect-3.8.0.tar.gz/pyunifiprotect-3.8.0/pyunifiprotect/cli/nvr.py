from dataclasses import dataclass
from datetime import timedelta

import typer

from pyunifiprotect.cli.base import CliContext, print_unifi_obj, protect_url, run
from pyunifiprotect.data import NVR

app = typer.Typer()

ARG_TIMEOUT = typer.Argument(..., help="Timeout (in seconds)")
ARG_DOORBELL_MESSAGE = typer.Argument(..., help="ASCII only. Max length 30")


@dataclass
class NVRContext(CliContext):
    device: NVR


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    UniFi Protect NVR CLI.

    Return NVR object without any arguments passed.
    """

    context = NVRContext(
        protect=ctx.obj.protect, device=ctx.obj.protect.bootstrap.nvr, output_format=ctx.obj.output_format
    )
    ctx.obj = context

    if not ctx.invoked_subcommand:
        print_unifi_obj(context.device)


app.command()(protect_url)


@app.command()
def set_default_reset_timeout(ctx: typer.Context, timeout: int = ARG_TIMEOUT) -> None:
    """
    Sets default message reset timeout.

    This is how long until a custom message is reset back to the default message if no
    timeout is passed in when the custom message is set.
    """

    nvr: NVR = ctx.obj.device
    run(ctx, nvr.set_default_reset_timeout(timedelta(seconds=timeout)))
    print_unifi_obj(nvr.doorbell_settings)


@app.command()
def set_default_doorbell_message(ctx: typer.Context, msg: str = ARG_DOORBELL_MESSAGE) -> None:
    """
    Sets default message for doorbell.

    This is the message that is set when a custom doorbell message times out or an empty
    one is set.
    """

    nvr: NVR = ctx.obj.device
    run(ctx, nvr.set_default_doorbell_message(msg))
    print_unifi_obj(nvr.doorbell_settings)


@app.command()
def add_custom_doorbell_message(ctx: typer.Context, msg: str = ARG_DOORBELL_MESSAGE) -> None:
    """Adds a custom doorbell message."""

    nvr: NVR = ctx.obj.device
    run(ctx, nvr.add_custom_doorbell_message(msg))
    print_unifi_obj(nvr.doorbell_settings)


@app.command()
def remove_custom_doorbell_message(ctx: typer.Context, msg: str = ARG_DOORBELL_MESSAGE) -> None:
    """Removes a custom doorbell message."""

    nvr: NVR = ctx.obj.device
    run(ctx, nvr.remove_custom_doorbell_message(msg))
    print_unifi_obj(nvr.doorbell_settings)
