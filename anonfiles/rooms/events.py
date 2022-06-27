from flask import request, g
from flask_socketio import join_room, leave_room, rooms, emit, disconnect
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room, add_user, \
    add_user_room, get_rooms, is_logged
from anonfiles import cache
from anonfiles.errors.handle_all import Halt
from anonfiles.utils.validations import validator


@io.on('try_room', namespace='/user')
def try_room(message):
    print('in try_room')
    room_name = message.get('name')
    room_pass = message.get('pass')
    is_room = cache.get(room_name)
    user = cache.get(str(request.sid), str(request.sid))
    logged_in = is_logged(user, str(request.sid))
    password = None if (room_name is None) or (is_room is None) else is_room[
        "pass"]
    print(room_name, password, is_room)
    if user in is_room["users"]:
        raise Halt(1011, "user is already in this room")
    if password and room_pass == password:

        join_room(room_name)
        add_user_room(cache, room_name, user, logged_in=logged_in)
        print(f'\nusers {request.sid}'
              f'\nrooms:{rooms()}')
        emit("joined", {"user": user, "room": room_name},
             to=room_name, include_self=True)
    else:
        print('emitting message')
        raise Halt(1011, "incorrect password")


@io.on('connect', namespace='/user')
@validator
def connection(client):
    print('client', client)
    print(request.sid)
    if g.payload:
        add_user(cache, request.sid, g.payload.get('sub'))


@io.on('disconnect', namespace='/user')
def disconnection():
    print('client disconnected')


@io.on('make_room', namespace='/user')
def make_room():
    user = cache.get(str(request.sid), str(request.sid))
    logged_in = is_logged(user, str(request.sid))
    room, password = create_room(cache)
    print("rooms", rooms())
    print('room_name_cached', room)
    print('password', password)
    join_room(room)
    add_user_room(cache, room, user, admin=True, logged_in=logged_in)
    emit('created', {'room': room, 'password': password})


@io.on('get_rooms', namespace='/user')
def get_all_rooms():
    print('here are current rooms', rooms())
    emit('all_rooms', get_rooms(cache, str(request.sid)))


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

