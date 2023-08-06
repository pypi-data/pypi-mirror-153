import asyncio
import base64
import json
import logging
from pathlib import Path
import sys
from typing import Optional, cast

import typer

from pyunifiprotect.api import ProtectApiClient
from pyunifiprotect.cli.base import CliContext
from pyunifiprotect.cli.nvr import app as nvr_app
from pyunifiprotect.data import WSPacket
from pyunifiprotect.test_util import SampleDataGenerator
from pyunifiprotect.utils import profile_ws as profile_ws_job

_LOGGER = logging.getLogger("pyunifiprotect")

try:
    from IPython import embed  # type: ignore
    from termcolor import colored
    from traitlets.config import get_config
except ImportError:
    embed = termcolor = get_config = None  # type: ignore

OPTION_USERNAME = typer.Option(
    ...,
    "--username",
    "-U",
    help="Unifi Protect Username",
    prompt=True,
    envvar="UFP_USERNAME",
)
OPTION_PASSWORD = typer.Option(
    ...,
    "--password",
    "-P",
    help="Unifi Protect password",
    prompt=True,
    hide_input=True,
    envvar="UFP_PASSWORD",
)
OPTION_ADDRESS = typer.Option(
    ...,
    "--address",
    "-a",
    prompt=True,
    help="Unifi Protect IP address or hostname",
    envvar="UFP_ADDRESS",
)
OPTION_PORT = typer.Option(443, "--port", "-p", help="Unifi Protect Port", envvar="UFP_PORT")
OPTION_SECONDS = typer.Option(15, "--seconds", "-s", help="Seconds to pull events")
OPTION_VERIFY = typer.Option(True, "--verify", "-v", help="Verify SSL", envvar="UFP_SSL_VERIFY")
OPTION_ANON = typer.Option(True, "--actual", help="Do not anonymize test data")
OPTION_ZIP = typer.Option(False, "--zip", help="Zip up data after generate")
OPTION_WAIT = typer.Option(30, "--wait", "-w", help="Time to wait for Websocket messages")
OPTION_OUTPUT = typer.Option(
    None,
    "--output",
    "-o",
    help="Output folder, defaults to `tests` folder one level above this file",
    envvar="UFP_SAMPLE_DIR",
)
OPTION_WS_FILE = typer.Option(None, "--file", "-f", help="Path or raw binary Websocket message")
ARG_WS_DATA = typer.Argument(None, help="base64 encoded Websocket message")

SLEEP_INTERVAL = 2


app = typer.Typer()
app.add_typer(nvr_app, name="nvr")


@app.callback()
def main(
    ctx: typer.Context,
    username: str = OPTION_USERNAME,
    password: str = OPTION_PASSWORD,
    address: str = OPTION_ADDRESS,
    port: int = OPTION_PORT,
    verify: bool = OPTION_VERIFY,
) -> None:
    """UniFi Protect CLI"""

    protect = ProtectApiClient(address, port, username, password, verify_ssl=verify)

    async def update() -> None:
        protect._bootstrap = await protect.get_bootstrap()  # pylint: disable=protected-access
        await protect.close_session()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(update())
    ctx.obj = CliContext(protect=protect)


def _setup_logger(level: int = logging.DEBUG, show_level: bool = False) -> None:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    if show_level:
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(formatter)
    _LOGGER.setLevel(logging.DEBUG)
    _LOGGER.addHandler(console_handler)


async def _progress_bar(wait_time: int, label: str) -> None:
    with typer.progressbar(range(wait_time // SLEEP_INTERVAL), label=label) as progress:
        for i in progress:
            if i > 0:
                await asyncio.sleep(SLEEP_INTERVAL)


@app.command()
def shell(ctx: typer.Context) -> None:
    """
    Opens ipython shell with Protect client initialized.

    Requires the `shell` extra to also be installed.
    """

    if embed is None or colored is None:
        typer.echo("ipython and termcolor required for shell subcommand")
        sys.exit(1)

    protect = cast(ProtectApiClient, ctx.obj.protect)  # pylint: disable=unused-variable # noqa
    _setup_logger(show_level=True)

    c = get_config()  # type: ignore
    c.InteractiveShellEmbed.colors = "Linux"
    embed(header=colored("protect = ProtectApiClient(*args)", "green"), config=c, using="asyncio")


@app.command()
def generate_sample_data(
    ctx: typer.Context,
    anonymize: bool = OPTION_ANON,
    wait_time: int = OPTION_WAIT,
    output_folder: Optional[Path] = OPTION_OUTPUT,
    do_zip: bool = OPTION_ZIP,
) -> None:
    """Generates sample data for UniFi Protect instance."""

    protect = cast(ProtectApiClient, ctx.obj.protect)

    if output_folder is None:
        tests_folder = Path(__file__).parent.parent / "tests"

        if not tests_folder.exists():
            typer.secho("Output folder required when not in dev-mode", fg="red")
            sys.exit(1)
        output_folder = (tests_folder / "sample_data").absolute()

    def log(msg: str) -> None:
        typer.echo(msg)

    def log_warning(msg: str) -> None:
        typer.secho(msg, fg="yellow")

    SampleDataGenerator(
        protect,
        output_folder,
        anonymize,
        wait_time,
        log=log,
        log_warning=log_warning,
        ws_progress=_progress_bar,
        do_zip=do_zip,
    ).generate()


@app.command()
def profile_ws(
    ctx: typer.Context,
    wait_time: int = OPTION_WAIT,
    output_path: Optional[Path] = OPTION_OUTPUT,
) -> None:
    """Profiles Websocket messages for UniFi Protect instance."""

    protect = cast(ProtectApiClient, ctx.obj.protect)

    async def callback() -> None:
        await protect.update()
        await profile_ws_job(protect, wait_time, output_path=output_path, ws_progress=_progress_bar)

    _setup_logger()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(callback())


@app.command()
def decode_ws_msg(ws_file: typer.FileBinaryRead = OPTION_WS_FILE, ws_data: Optional[str] = ARG_WS_DATA) -> None:
    """Decodes a base64 encoded UniFi Protect Websocket binary message."""

    if ws_file is None and ws_data is None:
        typer.secho("Websocket data required", fg="red")
        sys.exit(1)

    ws_data_raw = b""
    if ws_file is not None:
        ws_data_raw = ws_file.read()
    elif ws_data is not None:
        ws_data_raw = base64.b64decode(ws_data.encode("utf8"))

    packet = WSPacket(ws_data_raw)
    response = {"action": packet.action_frame.data, "data": packet.data_frame.data}

    typer.echo(json.dumps(response))
