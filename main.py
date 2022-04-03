from flask import Flask, request, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from config.init_config import init_config
from flask_caching import Cache
from anonfiles.models.room_specs import create_room

app = Flask(__name__)

get_config = init_config()
app.config.from_object(get_config)

io = SocketIO(app)

Session(app)
cache = Cache(app)


@io.on('connect', namespace='/user')
def create_room(socket):
    print(socket)
    room, password = create_room(cache)
    join_room(room)
    emit('created', {'room': room, 'password': password}, to=room, json=True)


@io.on('join', namespace='/user')
def join_room(data):
    password = cache.get(data["name"])
    if password is None or data["password"] is None:
        emit("incorrect")

    elif data["password"] == password:
        join_room(data["name"])
        emit("joined")
    else:
        emit("incorrect")


@io.on('leave', namespace='/user')
def leave_room(data):
    room = data['name']
    leave_room(room)
    emit("left")


if __name__ == "__main__":
    io.run(app, host="127.0.0.1", port=8080, threading=True)
    #app.run()


