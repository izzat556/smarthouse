# Home Assistant Device Reporter

Custom integration for Home Assistant to connect with an external server via WebSocket.

## Features
- Connects to your server (`ws://your-server-ip:8081/ws`).
- Receives JSON commands:
  ```json
  { "entity_id": "switch.living_room_lamp", "action": "on" }

