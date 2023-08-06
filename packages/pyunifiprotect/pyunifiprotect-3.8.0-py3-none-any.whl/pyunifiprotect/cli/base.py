import asyncio
from dataclasses import dataclass
from enum import Enum
import json
from typing import Any, Callable, Coroutine, Mapping

import typer

from pyunifiprotect.api import ProtectApiClient
from pyunifiprotect.data import NVR, ProtectAdoptableDeviceModel, ProtectBaseObject


class OutputFormatEnum(str, Enum):
    JSON = "json"
    PLAIN = "plain"


@dataclass
class CliContext:
    protect: ProtectApiClient
    output_format: OutputFormatEnum


def run(ctx: typer.Context, func: Coroutine[Any, Any, None]) -> None:
    """Helper method to call async function and clean up API client"""

    async def callback() -> None:
        await func
        await ctx.obj.protect.close_session()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(callback())


def json_output(obj: Any) -> None:
    typer.echo(json.dumps(obj, indent=2))


def print_unifi_obj(obj: ProtectBaseObject) -> None:
    """Helper method to print a single protect object"""

    json_output(obj.unifi_dict())


def print_unifi_dict(objs: Mapping[str, ProtectBaseObject]) -> None:
    """Helper method to print a dictionary of protect objects"""

    data = {}
    for key, obj in objs.items():
        data[key] = obj.unifi_dict()

    json_output(data)


def list_ids(ctx: typer.Context) -> None:
    """Prints list of id: name for each device."""

    objs: dict[str, ProtectAdoptableDeviceModel] = ctx.obj.devices
    to_print: list[tuple[str, str | None]] = []
    for obj in objs.values():
        to_print.append((obj.id, obj.name))

    if ctx.obj.output_format == OutputFormatEnum.JSON:
        json_output(to_print)
    else:
        for item in to_print:
            typer.echo(f"{item[0]}\t{item[1]}")


def protect_url(ctx: typer.Context) -> None:
    """Gets UniFi Protect management URL."""

    obj: NVR | ProtectAdoptableDeviceModel = ctx.obj.device
    if ctx.obj.output_format == OutputFormatEnum.JSON:
        json_output(obj.protect_url)
    else:
        typer.echo(obj.protect_url)


def is_wired(ctx: typer.Context) -> None:
    """Returns if the device is wired or not."""

    obj: ProtectAdoptableDeviceModel = ctx.obj.device
    json_output(obj.is_wired)


def is_wifi(ctx: typer.Context) -> None:
    """Returns if the device has WiFi or not."""

    obj: ProtectAdoptableDeviceModel = ctx.obj.device
    json_output(obj.is_wifi)


def is_bluetooth(ctx: typer.Context) -> None:
    """Returns if the device has Bluetooth or not."""

    obj: ProtectAdoptableDeviceModel = ctx.obj.device
    json_output(obj.is_bluetooth)


def bridge(ctx: typer.Context) -> None:
    """Returns bridge device if connected via Bluetooth."""

    obj: ProtectAdoptableDeviceModel = ctx.obj.device
    json_output(obj.bridge)


def set_ssh(ctx: typer.Context, enabled: bool) -> None:
    """
    Sets the isSshEnabled value for device.

    May not have an effect on many device types. Only seems to work for
    Linux and BusyBox based devices (camera, light and viewport).
    """

    obj: ProtectAdoptableDeviceModel = ctx.obj.device
    run(ctx, obj.set_ssh(enabled))


def reboot(ctx: typer.Context) -> None:
    """Reboots the device."""

    obj: ProtectAdoptableDeviceModel = ctx.obj.device
    run(ctx, obj.reboot())


def init_common_commands(app: typer.Typer) -> tuple[dict[str, Callable[..., Any]], dict[str, Callable[..., Any]]]:
    deviceless_commands: dict[str, Callable[..., Any]] = {}
    device_commands: dict[str, Callable[..., Any]] = {}

    deviceless_commands["list-ids"] = app.command()(list_ids)
    device_commands["protect-url"] = app.command()(protect_url)
    device_commands["is-wired"] = app.command()(is_wired)
    device_commands["is-wifi"] = app.command()(is_wifi)
    device_commands["is-bluetooth"] = app.command()(is_bluetooth)
    device_commands["bridge"] = app.command()(bridge)
    device_commands["set-ssh"] = app.command()(set_ssh)
    device_commands["reboot"] = app.command()(reboot)

    return deviceless_commands, device_commands
