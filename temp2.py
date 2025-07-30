# import asyncio
# import json
# import uuid
# import websockets

# # Keep track of connected clients by ID
# clients: dict[str, websockets.WebSocketServerProtocol] = {}


# async def handler(websocket):
#     # 1. Assign a unique ID and store the socket
#     client_id = str(uuid.uuid4())
#     clients[client_id] = websocket

#     # 2. Tell the newcomer its ID and the list of existing peers
#     peers = [pid for pid in clients if pid != client_id]
#     await websocket.send(json.dumps({
#         "type": "id",
#         "id": client_id,
#         "peers": peers
#     }))
#     print(f"[+] {client_id} connected; peers: {peers}")

#     # 3. Notify everyone else about the newcomer
#     notice = json.dumps({"type": "peer-connected", "id": client_id})
#     for pid, ws in clients.items():
#         if pid != client_id:
#             await ws.send(notice)

#     try:
#         # 4. Relay all "signal" messages one-to-one
#         async for raw in websocket:
#             msg = json.loads(raw)
#             if msg.get("type") == "signal":
#                 target = msg.get("to")
#                 if target in clients:
#                     await clients[target].send(raw)

#     except websockets.exceptions.ConnectionClosed:
#         pass

#     finally:
#         # 5. Clean up on disconnect
#         del clients[client_id]
#         leave = json.dumps({"type": "peer-disconnected", "id": client_id})
#         for ws in clients.values():
#             await ws.send(leave)
#         print(f"[-] {client_id} disconnected")


# async def main():
#     print("[*] Signaling server listening on ws://0.0.0.0:8765")
#     async with websockets.serve(handler, "0.0.0.0", 8765):
#         await asyncio.Future()  # run forever


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
import json
import uuid
import websockets

# Keep track of connected clients by ID
clients: dict[str, websockets.WebSocketServerProtocol] = {}


async def handler(websocket):
    # 1. Assign a unique ID and store the socket
    client_id = str(uuid.uuid4())
    clients[client_id] = websocket

    # 2. Tell the newcomer its ID and the list of existing peers
    peers = [pid for pid in clients if pid != client_id]
    await websocket.send(json.dumps({
        "type": "id",
        "id": client_id,
        "peers": peers
    }))
    print(f"[+] {client_id} connected; peers: {peers}")

    # 3. Notify everyone else about the newcomer
    notice = json.dumps({"type": "peer-connected", "id": client_id})
    for pid, ws in clients.items():
        if pid != client_id:
            await ws.send(notice)

    try:
        # 4. Relay all "signal" messages one-to-one
        async for raw in websocket:
            msg = json.loads(raw)
            if msg.get("type") == "signal":
                target = msg.get("to")
                if target in clients:
                    await clients[target].send(raw)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        # 5. Clean up on disconnect
        del clients[client_id]
        leave = json.dumps({"type": "peer-disconnected", "id": client_id})
        for ws in clients.values():
            await ws.send(leave)
        print(f"[-] {client_id} disconnected")


async def main():
    print("[*] Signaling server listening on ws://0.0.0.0:8765")

    # Disable ping/pong timeouts so idle connections never get dropped
    async with websockets.serve(
        handler,
        "0.0.0.0",
        8765,
        ping_interval=None,
        ping_timeout=None
    ):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
