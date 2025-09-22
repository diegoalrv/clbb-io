import json
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

from backend.services.layer import set_layer_visibility

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
        elif action_type == 'set_layer_visibility':
            layer_id = data.get('layer_id')
            on = data.get('on')

            updated_layer_config = await database_sync_to_async(set_layer_visibility)(layer_id, on)

            if updated_layer_config:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'set_layer_visibility',
                        'sender': self.channel_name,
                        'content': {
                            'id': layer_id,
                            'config': {
                                'on': updated_layer_config.config['on']
                            }
                        }
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Layer {layer_id} not found'
                }))
        # elif action_type == 'set_layer_config':
        #     layer_id = data.get('layer_id')
        #     config = data.get('config')

        #     updated_layer_config = await database_sync_to_async(set_layer_config)(layer_id, config)

        #     if updated_layer_config:
        #         await self.channel_layer.group_send(
        #             self.room_group_name,
        #             {
        #                 'type': 'set_layer_config',
        #                 'sender': self.channel_name,
        #                 'content': {
        #                     'id': layer_id,
        #                     'config': updated_layer_config.config
        #                 }
        #             }
        #         )
        #     else:
        #         await self.send(text_data=json.dumps({
        #             'type': 'error',
        #             'message': f'Layer {layer_id} not found'
        #         }))

    async def set_layer_visibility(self, event):
        if event['sender'] == self.channel_name:
            return  # Don't echo back to sender

        await self.send(text_data=json.dumps({
            'type': 'layer_update',
            'content': event['content']
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
