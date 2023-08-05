"""Handle MySensors messages."""
from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any

from mysensors import Message

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.util import decorator

from .const import CHILD_CALLBACK, NODE_CALLBACK, DevId, GatewayId
from .device import get_mysensors_devices
from .helpers import discover_mysensors_platform, validate_set_msg

HANDLERS: decorator.Registry[
    str, Callable[[HomeAssistant, GatewayId, Message], Coroutine[Any, Any, None]]
] = decorator.Registry()


@HANDLERS.register("set")
async def handle_set(hass: HomeAssistant, gateway_id: GatewayId, msg: Message) -> None:
    """Handle a mysensors set message."""
    validated = validate_set_msg(gateway_id, msg)
    _handle_child_update(hass, gateway_id, validated)


@HANDLERS.register("internal")
async def handle_internal(
    hass: HomeAssistant, gateway_id: GatewayId, msg: Message
) -> None:
    """Handle a mysensors internal message."""
    internal = msg.gateway.const.Internal(msg.sub_type)
    if (handler := HANDLERS.get(internal.name)) is None:
        return
    await handler(hass, gateway_id, msg)


@HANDLERS.register("I_BATTERY_LEVEL")
async def handle_battery_level(
    hass: HomeAssistant, gateway_id: GatewayId, msg: Message
) -> None:
    """Handle an internal battery level message."""
    _handle_node_update(hass, gateway_id, msg)


@HANDLERS.register("I_HEARTBEAT_RESPONSE")
async def handle_heartbeat(
    hass: HomeAssistant, gateway_id: GatewayId, msg: Message
) -> None:
    """Handle an heartbeat."""
    _handle_node_update(hass, gateway_id, msg)


@HANDLERS.register("I_SKETCH_NAME")
async def handle_sketch_name(
    hass: HomeAssistant, gateway_id: GatewayId, msg: Message
) -> None:
    """Handle an internal sketch name message."""
    _handle_node_update(hass, gateway_id, msg)


@HANDLERS.register("I_SKETCH_VERSION")
async def handle_sketch_version(
    hass: HomeAssistant, gateway_id: GatewayId, msg: Message
) -> None:
    """Handle an internal sketch version message."""
    _handle_node_update(hass, gateway_id, msg)


@callback
def _handle_child_update(
    hass: HomeAssistant, gateway_id: GatewayId, validated: dict[Platform, list[DevId]]
) -> None:
    """Handle a child update."""
    signals: list[str] = []

    # Update all platforms for the device via dispatcher.
    # Add/update entity for validated children.
    for platform, dev_ids in validated.items():
        devices = get_mysensors_devices(hass, platform)
        new_dev_ids: list[DevId] = []
        for dev_id in dev_ids:
            if dev_id in devices:
                signals.append(CHILD_CALLBACK.format(*dev_id))
            else:
                new_dev_ids.append(dev_id)
        if new_dev_ids:
            discover_mysensors_platform(hass, gateway_id, platform, new_dev_ids)
    for signal in set(signals):
        # Only one signal per device is needed.
        # A device can have multiple platforms, ie multiple schemas.
        async_dispatcher_send(hass, signal)


@callback
def _handle_node_update(
    hass: HomeAssistant, gateway_id: GatewayId, msg: Message
) -> None:
    """Handle a node update."""
    signal = NODE_CALLBACK.format(gateway_id, msg.node_id)
    async_dispatcher_send(hass, signal)
