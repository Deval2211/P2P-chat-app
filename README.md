# P2P Chat App

A simple peer-to-peer chat application using WebRTC for direct messaging and WebSockets for signaling. Users can join a global chat or create/join private rooms.

## Features

- Secure P2P messaging (WebRTC DataChannels)
- Real-time communication
- Global and private chat rooms
- Modern, responsive UI

### Using the App

1. Open `index.html` in your browser.
2. Enter your display name and continue.
3. Choose a chat room (global or private).
4. Start chatting!

## Project Structure

- [`server.py`](server.py): Python WebSocket signaling server
- [`index.html`](index.html): Welcome page
- [`lobby.html`](lobby.html): Room selection page
- [`chatRoom.html`](chatRoom.html): Chat interface
- [`ui.css`](ui.css): Stylesheet

## Dependencies

- websockets
- aiohttp
- aiortc
- asyncio
- requests

See [pyproject.toml](pyproject.toml) for details.
