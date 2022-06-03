from flask_socketio import SocketIO, join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room
from anonfiles import cache


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

