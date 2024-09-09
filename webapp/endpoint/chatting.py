import starlette.websockets
from fastapi import WebSocket, APIRouter, Query
from webapp.common.util.token_decoder import decode_token
from webapp.common.exceptions import auth
from webapp.domain.user.persistance.user_dao import MySQLUserDao
from webapp.common.src.user_container import UserContainer


class ConnectionManager:
    def __init__(self):
        self.groups: dict[list[WebSocket]] = {}

    async def connect(self, group_id, websocket: WebSocket):
        await websocket.accept()
        try:
            self.groups[group_id].append(websocket)
        except KeyError:
            self.groups[group_id] = [websocket]

    def disconnect(self, group_id, websocket: WebSocket):
        self.groups[group_id].remove(websocket)
        if len(self.groups[group_id]) == 0:
            self.groups.pop(group_id)

    async def broadcast(self, group_id, message):
        for connection in self.groups[group_id]:
            await connection.send_json(message)


manager = ConnectionManager()

ws_router = APIRouter(prefix='/taxi')


@ws_router.websocket("/{group_id}")
async def websocket_endpoint(group_id: str,
                             websocket: WebSocket,
                             token: str = Query(),
                             db: MySQLUserDao = UserContainer.user_dao):
    try:
        user_id = int(decode_token(token)['id'])
    except auth.TokenExpired:
        await websocket.close(1008, 'Unauthorized')
        return

    user = db.find_user_by_id(user_id)

    await manager.connect(group_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            data = {
                'user': user.json,
                'message': data['message']
            }
            await manager.broadcast(group_id, data)
    except starlette.websockets.WebSocketDisconnect:
        manager.disconnect(group_id, websocket)
