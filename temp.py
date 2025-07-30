# # import socket
# # import json
# # from  aiortc import RTCPeerConnection, RTCSessionDescription
# # import asyncio

# # info = {
# #     'from': 'parth',
# #     'to': 'deval'
# # }
# # json_info = json.dumps(info)


# # async def main():
# #     pc = RTCPeerConnection()

# #     dc = pc.createDataChannel('data')
# #     @dc.on('open')
# #     def on_open():
# #         print("data channel is open")

# #     @dc.on("message")
# #     def on_msg(msg):
# #         print(f'recieved: {msg}')


# #     offer = await pc.createOffer()
    
# #     offer_desc = RTCSessionDescription(sdp=offer.__dict__['sdp'], type='offer')
# #     await pc.setLocalDescription(offer_desc)

# #     info['sdp'] = offer.__dict__

# #     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     client.connect(('127.0.0.1', 9000))

# #     json_info = json.dumps(info)

# #     client.send(json_info.encode())

# #     answer = json.loads(client.recv(2024).decode())
# #     answer_desc = RTCSessionDescription(sdp=answer['sdp'], type='answer')

# #     await pc.setRemoteDescription(answer_desc)

# #     print(dc.readyState)
# #     # dc.send('hellow')

# # if __name__ == "__main__":
# #     asyncio.run(main())

import asyncio
import json
import socket
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate

async def main():
    # 1) TCP “signaling” channel
    client = socket.socket()
    client.connect(("15.206.147.88", 8765))

    pc = RTCPeerConnection()

    # 2) Create our data channel
    dc = pc.createDataChannel("data")

    @dc.on("open")
    def on_open():
        print("Client: data channel open")
        dc.send("fuck your mom")

    @dc.on("message")
    def on_message(msg):
        print("Client received:", msg)

    # 3) Send ICE candidates as we gather them
    @pc.on("icecandidate")
    def on_icecandidate(event):
        payload = {
            "type": "ice",
            "candidate": None if event.candidate is None else {
                "candidate": event.candidate.to_sdp(),
                "sdpMid": event.candidate.sdpMid,
                "sdpMLineIndex": event.candidate.sdpMLineIndex,
            }
        }
        client.send((json.dumps(payload) + "\n").encode())

    # 4) Create offer, set it, then send it
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    client.send((json.dumps({
        "type": "offer",
        "sdp": {
            "type": pc.localDescription.type,
            "sdp": pc.localDescription.sdp
        }
    }) + "\n").encode())

    # 5) Receive answer
    data = await asyncio.get_event_loop().run_in_executor(None, client.recv, 4096)
    msg = json.loads(data.decode())
    answer = RTCSessionDescription(sdp=msg["sdp"]["sdp"], type=msg["sdp"]["type"])
    await pc.setRemoteDescription(answer)

    # 6) Consume ICE candidates from server
    while True:
        data = await asyncio.get_event_loop().run_in_executor(None, client.recv, 4096)
        msg = json.loads(data.decode())
        if msg["type"] == "ice":
            if msg["candidate"] is None:
                break  # server finished sending candidates
            ice = msg["candidate"]
            cand = RTCIceCandidate(
                candidate=ice["candidate"],
                sdpMid=ice["sdpMid"],
                sdpMLineIndex=ice["sdpMLineIndex"]
            )
            await pc.addIceCandidate(cand)

    # let the data channel do its thing
    await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
