# P2P Chat App

A simple peer-to-peer chat application using WebRTC for direct messaging and WebSockets for signaling. Users can join a global chat or create/join private rooms.

## Features

- Secure P2P messaging (WebRTC DataChannels)
- Real-time communication
- Global and private chat rooms
- Modern, responsive UI

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js (optional, for frontend tooling)

### Installation

1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd p2pProject
   ```

2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or use [pyproject.toml](pyproject.toml) with Poetry:
   ```sh
   poetry install
   ```

### Running the Server

Start the signaling server:
```sh
python server.py
```
The server listens on `ws://0.0.0.0:8765`.

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
