from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.websockets import WebSocketState
from fastapi_sqlalchemy import DBSessionMiddleware, db
from BDD.models import Coordonnee
from BDD.schema import Coordonnee  as Model_coordonnee
import os
from dotenv import load_dotenv

date_format = '%Y-%m-%d %H:%M:%S'

load_dotenv('.env')

ws_connections = []

def get_connections() :
    return ws_connections 

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/coordonnees/{ip}')
async def get_coordonnees(ip):
    coor = db.session.query(Coordonnee).filter(Coordonnee.ip == ip).all()
    return coor

@app.post('/coordonnees')
async def add_coordonnees(coor: Model_coordonnee, connections= Depends(get_connections)):
    db_coor = Coordonnee(latitude = coor.latitude, longitude = coor.longitude, ip = coor.ip, date = datetime.strptime(coor.date, date_format))
    db.session.add(db_coor)
    db.session.commit()

    for i in range(len(connections)):
        if connections[i].client_state == WebSocketState.DISCONNECTED :
            connections.remove(connections[i])
        else :
            await connections[i].send_json({'latitude': coor.latitude, 'longitude':coor.longitude, 'ip': coor.ip, 'date': coor.date})
    return True

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, connections = Depends(get_connections)):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json(data)
    except WebSocketDisconnect :
        connections.remove(websocket)