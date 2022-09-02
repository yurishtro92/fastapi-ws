from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

with open('templates/empty.html', 'r') as f:
    form = f.read()


@app.get("/")
async def root():
    return HTMLResponse(form)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive()
        if data['text'] != 'end':
            await websocket.send_json(data['text'])
        else:
            await websocket.send_json('End of work, please press F5 to restart')
            return


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
