import asyncio
import pathlib
import ssl
import sys
import websockets
REMOTEURL = None
LOCALHOST = None
LOCALPORT = None
async def all(websocket: websockets.WebSocketClientProtocol):
    print("connected from", websocket.remote_address, websocket.path)
    async with websockets.connect(REMOTEURL+websocket.path) as websocket2:
        while True:
            try:
                async def remote2local():
                    while True:
                        data = await websocket2.recv()
                        print(f"<<< {data}")
                        await websocket.send(data)
                async def local2remote():
                    while True:
                        data = await websocket.recv()
                        print(f">>> {data}")
                        await websocket2.send(data)
                await asyncio.gather(remote2local(), local2remote())
            except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError):
                print("closed connection")
                break

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="cert.pem")

async def main():
    async with websockets.serve(all, LOCALHOST, LOCALPORT, ssl=ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    REMOTEURL = sys.argv[1]
    LOCALHOST = sys.argv[2]
    LOCALPORT = sys.argv[3]
    asyncio.run(main())