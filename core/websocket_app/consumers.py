import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Aquí puedes validar origen, auth, etc.
        await self.accept()
        await self.send_json({"type": "welcome", "message": "WebSocket conectado"})

    async def receive(self, text_data=None, bytes_data=None):
        # Loguea lo que llega (ahí “lees” el mensaje)
        logger.info(f"[WS] text={text_data!r} bytes={bool(bytes_data)}")

        # Intenta parsear JSON si viene en texto
        payload = None
        if text_data is not None:
            try:
                payload = json.loads(text_data)
            except json.JSONDecodeError:
                payload = {"raw": text_data}

        # Respuesta simple tipo echo
        await self.send_json({"type": "echo", "received": payload})

    async def disconnect(self, close_code):
        logger.info(f"[WS] desconectado code={close_code}")

    # Helper para enviar JSON
    async def send_json(self, obj: dict):
        await self.send(text_data=json.dumps(obj))

class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
