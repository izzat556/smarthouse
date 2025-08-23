import logging
import asyncio
import json
import websockets

DOMAIN = "device_reporter"
_LOGGER = logging.getLogger(__name__)

# ⚡ Укажи IP своего сервера
SERVER_WS_URL = "ws://localhost:1723"

async def async_setup(hass, config):
    """Set up WebSocket connection to external server."""

    async def listen_to_server():
        while True:
            try:
                _LOGGER.info("Connecting to server WebSocket %s", SERVER_WS_URL)
                async with websockets.connect(SERVER_WS_URL) as websocket:
                    _LOGGER.info("Connected to server")
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            entity_id = data.get("entity_id")
                            action = data.get("action")

                            if entity_id and action in ["on", "off"]:
                                service = "turn_on" if action == "on" else "turn_off"
                                await hass.services.async_call(
                                    "switch",
                                    service,
                                    {"entity_id": entity_id},
                                    blocking=True
                                )
                                _LOGGER.info("Executed %s on %s", action, entity_id)
                            else:
                                _LOGGER.warning("Invalid command: %s", data)
                        except Exception as e:
                            _LOGGER.error("Error handling message: %s", e)
            except Exception as e:
                _LOGGER.error("WebSocket connection error: %s", e)

            _LOGGER.info("Reconnecting in 5s...")
            await asyncio.sleep(5)

    hass.loop.create_task(listen_to_server())
    return True

