import json
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

from backend.services.data import set_config

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

        query_params = parse_qs(self.scope["query_string"].decode())
        self.client_role = query_params.get("role", ["unknown"])[0]

        # Register connection
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
        data = json.loads(text_data)
        action_type = data.get('type')

        if action_type == 'chat_message':
            message = data.get('message')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.channel_name
                }
            )
        elif action_type == 'set_config':
            layer_id = data.get('layer_id')
            content = data.get('content')

            updated_layer_config = await database_sync_to_async(set_config)(layer_id, content)

            if updated_layer_config:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'set_config',
                        'sender': self.channel_name,
                        'layer_id': layer_id,
                        'content': content
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Layer {layer_id} not found'
                }))
        elif action_type == 'set_playing':
            playing = data.get('playing')

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'set_playing',
                    'sender': self.channel_name,
                    'playing': playing
                }
            )
        elif action_type == 'set_time':
            time = data.get('time')

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'set_time',
                    'sender': self.channel_name,
                    'time': time
                }
            )

    async def set_config(self, event):
        if event['sender'] == self.channel_name:
            return  # Don't echo back to sender

        await self.send(text_data=json.dumps({
            'type': 'layer_update',
            'layer_id': event['layer_id'],
            'content': event['content']
        }))

    async def set_playing(self, event):
        if event['sender'] == self.channel_name:
            return  # Don't echo back to sender

        await self.send(text_data=json.dumps({
            'type': 'set_playing',
            'playing': event['playing']
        }))

    async def set_time(self, event):
        if event['sender'] == self.channel_name:
            return  # Don't echo back to sender

        await self.send(text_data=json.dumps({
            'type': 'set_time',
            'time': event['time']
        }))

    # Receive message from room group
    async def chat_message(self, event):
        if event['sender'] == self.channel_name:
            return  # Don't echo back to sender
        
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
