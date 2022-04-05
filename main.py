from flask import Flask, request, session
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, rooms, emit
from config.init_config import init_config
from flask_caching import Cache
from anonfiles.models.room_specs import create_room

app = Flask(__name__)

get_config = init_config()
app.config.from_object(get_config)

io = SocketIO(app, cors_allowed_origins="*")

Session(app)
cache = Cache(app)


@app.route('/join')
def try_room():
    data = request.args.get
    password = None if data("name") is None else cache.get(data("name"))
    if password is None or data("password") is None:
        return {"reason": "incorrect password or room"}

    if data("password") == password:
        join_room(data("name"))
        emit("joined")


@io.on('make_room', namespace='/user')
def make_room(socket):
    print('socket', socket)
    room, password = create_room(cache)
    print("rooms", rooms())
    join_room(room)
    emit('created', {'room': room, 'password': password})


@io.on('leave', namespace='/user')
def exit_room(data):
    room = data['name']
    leave_room(room)
    emit("left", {'room': room})


if __name__ == "__main__":
    io.run(app, host="127.0.0.1", port=8080)
    #app.run()


