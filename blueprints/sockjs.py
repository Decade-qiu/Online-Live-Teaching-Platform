import json
import datetime
import numpy as np
from sockjs.tornado import SockJSConnection
import tornado
from model.CRUD import CRUD


class ChatRoomHandler(SockJSConnection):
    waiters = set()
    def on_open(self, request):
        self.waiters.add(self)
    def on_message(self, message):
        try:
            data = json.loads(message)
            streamid = data.get('streamid', '')
            data['dt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            if data['code'] == 2:
                CRUD.save_msg(content, streamid)
            self.broadcast(self.waiters, content)
        except Exception as e:
            print(e)
    def on_close(self):
        self.waiters.remove(self)

class CanvasConnection(SockJSConnection):
    clients = set()
    def on_open(self, info):
        self.clients.add(self)
    def on_message(self, message):
        for client in self.clients:
            if client != self:
                client.send(message)
    def on_close(self):
        self.clients.remove(self)

class AudioHandler(SockJSConnection):   

    connections = set()

    def on_open(self, info):
        self.connections.add(self)
        print("open-audio")

    def on_message(self, message):
        print(message)
        for conn in self.connections:
            if conn != self:
                conn.send(message)

    def on_close(self):
        self.connections.remove(self)
        print("close-audio")

class checkHandler(SockJSConnection):   

    connections = set()

    def on_open(self, info):
        self.connections.add(self)
        print("open!!")

    def on_message(self, message):
        for conn in self.connections:
            if conn != self:
                conn.send(message)

    def on_close(self):
        self.connections.remove(self)
        print("close!!")