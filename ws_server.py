import asyncio
import websockets
import json
import threading

clients = set()
pending_config = None

async def handler(websocket):
    global pending_config
    clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get("type") == "save_config":
                    pending_config = data.get("data")
            except Exception:
                pass
    finally:
        clients.discard(websocket)

async def _start_server():
    async with websockets.serve(handler, "localhost", 5678):
        await asyncio.Future()

def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_start_server())

def run_in_background():
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

def broadcast(gesture, key):
    msg = json.dumps({"type": "gesture", "gesture": gesture, "key": key})
    to_remove = set()
    for ws in list(clients):
        try:
            asyncio.run(ws.send(msg))
        except Exception:
            to_remove.add(ws)
    clients.difference_update(to_remove)