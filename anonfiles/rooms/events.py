from flask import session, request
from flask_socketio import join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room, add_user
from anonfiles import cache
from anonfiles.errors.handle_all import Halt


@io.on('try_room', namespace='/user')
def try_room(message):
    print('in try_room')
    room_name = message.get('name')
    room_pass = message.get('pass')
    is_room = cache.get(room_name)

    password = None if (room_name is None) or (is_room is None) else is_room[
        "pass"]
    print(room_name, password, is_room)
    if str(request.sid) in is_room["users"]:
        raise Halt(1011, "user is already in this room")
    if password and room_pass == password:

        join_room(room_name)
        add_user(cache, room_name, str(request.sid))
        print(f'\nusers {request.sid}'
              f'\nrooms:{rooms()}')
        emit("joined", {"user": request.sid, "room": room_name},
             to=room_name, include_self=True)
    else:
        print('emitting message')
        raise Halt(1011, "incorrect password")


@io.on('connect', namespace='/user')
def connection(client):
    print('client', client)
    print(request.sid)


@io.on('make_room', namespace='/user')
def make_room():
    room, password = create_room(cache)
    print("rooms", rooms())
    print('room_name_cached', room)
    print('password', password)
    join_room(room)
    add_user(cache, room, str(request.sid), admin=True)
    emit('created', {'room': room, 'password': password})


@io.on('get_rooms', namespace='/user')
def get_all_rooms():
    print('here are current rooms', rooms())
    emit('all_rooms', rooms())


@io.on('get_users', namespace='/user')
def get_all_users(data):
    room_name = data["room"]
    room = cache.get(room_name)
    if room:
        emit('all_users', {"users": room["users"]}, to=room_name)
    else:
        raise Halt(1003, "error processing data")


@io.on('leave', namespace='/user')
def exit_room(data):
    room = data['name']
    leave_room(room)
    emit("left", {'room': room})

