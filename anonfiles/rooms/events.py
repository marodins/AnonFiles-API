from flask_socketio import join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room
from anonfiles import cache
from anonfiles.errors.handle_all import Halt


@io.on('try_room', namespace='/user')
def try_room(message):
    room_name = message.get('name', None)
    room_pass = message.get('pass', None)
    password = None if room_name is None else cache.get(room_name)
    if password is None or room_pass is None:
        raise Halt(404, "incorrect password or room")

    if room_pass == password:
        join_room(room_name)
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

