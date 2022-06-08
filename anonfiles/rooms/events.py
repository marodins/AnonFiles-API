from flask import session, request
from flask_socketio import join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room
from anonfiles import cache
from anonfiles.errors.handle_all import Halt


@io.on('try_room', namespace='/user')
def try_room(message):
    print('in try_room')
    room_name = message.get('name', None)
    room_pass = message.get('pass', None)
    is_room = cache.get(room_name)

    password = None if room_name is None or is_room is None else is_room

    if password and room_pass == password:
        join_room(room_name)
        emit("joined")
    else:
        print('emitting message')
        emit("message", {"error": "incorrect password"})


@io.on('connect', namespace='/user')
def connection(client):
    print('client', client)
    print(request.sid)


@io.on('make_room', namespace='/user')
def make_room(data):
    room, password = create_room(cache)
    print("rooms", rooms())
    print('room_name_cached', room)
    print(password)
    join_room(room)
    emit('created', {'room': room, 'password': password})


@io.on('get_rooms', namespace='/user')
def get_all_rooms():
    emit('all_rooms', rooms())


@io.on('leave', namespace='/user')
def exit_room(data):
    room = data['name']
    leave_room(room)
    emit("left", {'room': room})

