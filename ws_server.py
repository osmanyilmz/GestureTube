import asyncio
import websockets
import json
import threading

clients = set()
pending_config = None
current_config = {}
_loop = None

async def handler(websocket):
    global pending_config
    clients.add(websocket)
    try:
        if current_config:
            await websocket.send(json.dumps({"type": "load_config", "data": current_config}))
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
    global _loop
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    _loop.run_until_complete(_start_server())

def run_in_background():
    t = threading.Thread(target=start_server, daemon=True)
    t.start()

def set_config(config):
    global current_config
    current_config = config

def broadcast(gesture, key):
    if not _loop or not clients:
        return
    msg = json.dumps({"type": "gesture", "gesture": gesture, "key": key})
    async def _send():
        to_remove = set()
        for ws in list(clients):
            try:
                await ws.send(msg)
            except Exception:
                to_remove.add(ws)
        clients.difference_update(to_remove)
    asyncio.run_coroutine_threadsafe(_send(), _loop)