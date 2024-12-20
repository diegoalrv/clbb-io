import json
from channels.generic.websocket import WebsocketConsumer

class DashboardConsumer(WebsocketConsumer):
    connections = []

    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        self.connections.append(self)
        self.update_indicator(msg="Connected")

    def disconnect(self, code):
        self.update_indicator(msg="Disconnected")
        self.connections.remove(self)
        return super().disconnect(code)

    def update_indicator(self, msg):
        for connection in self.connections:
            connection.send(
                text_data=json.dumps(
                    {
                        "msg": f"{self.user} {msg}",
                        "online": f"{len(self.connections)}",
                        "users": [f"{user.scope['user']}" for user in self.connections],                        
                    }
                )
            )

    def receive(self, text_data):
        for connection in self.connections:
            connection.send(
                text_data=text_data
                # text_data=json.dumps(text_data)
            )
        pass

    def send_message(self, message):
        self.send(text_data=json.dumps({"message": message}))

    def broadcast(self, message):
        for connection in self.connections:
            connection.send(text_data=json.dumps({"message": message}))

class MapConsumer(WebsocketConsumer):
    connections = []

    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        self.connections.append(self)
        self.update_indicator(msg="Connected")

    def disconnect(self, code):
        self.update_indicator(msg="Disconnected")
        self.connections.remove(self)
        return super().disconnect(code)

    def update_indicator(self, msg):
        for connection in self.connections:
            connection.send(
                text_data=json.dumps(
                    {
                        "msg": f"{self.user} {msg}",
                        "online": f"{len(self.connections)}",
                        "users": [f"{user.scope['user']}" for user in self.connections],                        
                    }
                )
            )

    def receive(self, text_data):
        for connection in self.connections:
            connection.send(
                text_data=text_data
                # text_data=json.dumps(text_data)
            )
        pass

    def send_message(self, message):
        self.send(text_data=json.dumps({"message": message}))

    def broadcast(self, message):
        for connection in self.connections:
            connection.send(text_data=json.dumps({"message": message}))