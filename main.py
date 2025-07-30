# # import socket
# # import time
# # import json
# # from aiortc import RTCPeerConnection, RTCSessionDescription
# # import asyncio

# # async def main():
# #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     server.bind(("0.0.0.0", 9000))
# #     server.listen(5)

# #     rc = RTCPeerConnection()
# #     # dc = rc.createDataChannel('data')

# #     # @dc.on('open')
# #     # async def on_open():
# #     #     print('data channel opened!')

# #     # @dc.on('message')
# #     # async def on_msg(msg):
# #     #     print(f'got msg {msg}')


# #     @rc.on('datachannel')
# #     def on_datachannel(channel):
# #         @channel.on('open')
# #         def on_open():
# #             print('data channel opened on server!')

# #         @channel.on('message')
# #         def on_message(msg):
# #             print(f'got msg {msg}')

# #     while True:
# #         client, addr = server.accept()
# #         msg = json.loads(client.recv(2024).decode())
# #         fr = msg['from']
# #         to = msg['to']
# #         offer = msg['sdp']
        
# #         offer_desc = RTCSessionDescription(sdp=offer['sdp'], type='offer')

# #         offer = msg['sdp']
# #         await rc.setRemoteDescription(offer_desc)

# #         answer = await rc.createAnswer()
# #         await rc.setLocalDescription(answer)

# #         # answer_dict = answer.__dict__
# #         client.send(json.dumps(answer.__dict__).encode())

# # if __name__ == "__main__":
# #     asyncio.run(main())``

import asyncio
import json
import socket
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

async def handle_client(client):
    pc = RTCPeerConnection()

    # 1) Listen for an incoming data channel (don't create your own here)
    @pc.on("datachannel")
    def on_datachannel(dc):
        @dc.on("open")
        def on_open():
            print("Server: data channel open")

        @dc.on("message")
        def on_message(msg):
            print("Server received:", msg)
            dc.send("fuck you")

    # 2) Send each ICE candidate back to the client as it’s gathered
    @pc.on("icecandidate")
    def on_icecandidate(event):
        payload = {
            "type": "ice",
            # None candidate signals end‐of‐gathering
            "candidate": None if event.candidate is None else {
                "candidate": event.candidate.to_sdp(),
                "sdpMid": event.candidate.sdpMid,
                "sdpMLineIndex": event.candidate.sdpMLineIndex,
            }
        }
        client.send((json.dumps(payload) + "\n").encode())

    # 3) Receive the offer SDP
    data = await asyncio.get_event_loop().run_in_executor(None, client.recv, 4096)
    msg = json.loads(data.decode())
    offer = RTCSessionDescription(sdp=msg["sdp"]["sdp"], type=msg["sdp"]["type"])
    await pc.setRemoteDescription(offer)

    # 4) Create and send the answer SDP
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    response = {
        "type": "answer",
        "sdp": {
            "type": pc.localDescription.type,
            "sdp": pc.localDescription.sdp
        }
    }
    client.send((json.dumps(response) + "\n").encode())

    # 5) Receive ICE candidates from the client
    while True:
        data = await asyncio.get_event_loop().run_in_executor(None, client.recv, 4096)
        msg = json.loads(data.decode())
        if msg["type"] == "ice":
            if msg["candidate"] is None:
                break  # client finished sending candidates
            ice = msg["candidate"]
            cand = RTCIceCandidate(
                candidate=ice["candidate"],
                sdpMid=ice["sdpMid"],
                sdpMLineIndex=ice["sdpMLineIndex"]
            )
            await pc.addIceCandidate(cand)

    # keep the connection alive so the data channel can open
    await asyncio.sleep(30)


async def main():
    server_sock = socket.socket()
    server_sock.bind(("0.0.0.0", 8765))
    server_sock.listen(1)
    print("Server listening on port 9000")

    loop = asyncio.get_event_loop()
    while True:
        client, addr = await loop.run_in_executor(None, server_sock.accept)
        print("Client connected:", addr)
        asyncio.create_task(handle_client(client))

if __name__ == "__main__":
    asyncio.run(main())
