import os

# installed libs
from flask_socketio import SocketIO
from app import create_app

app = create_app("development")['app']
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)