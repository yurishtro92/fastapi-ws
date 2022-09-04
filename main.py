from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import json

app = FastAPI()

with open('templates/empty.html', 'r') as f:
    form = f.read()

@app.get("/")
async def root():
    return HTMLResponse(form)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 0
    while True:
        data = await websocket.receive()
        data_json = json.dumps(data)
        if data["text"] != 'end':
            i += 1
            await websocket.send_json(str(i) + '. ' + str(json.loads(data_json)['text']))
        else:
            await websocket.send_json('End of work, please press F5 to restart')
            return


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
