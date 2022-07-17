from flask import request, g
from flask_socketio import join_room, leave_room, rooms, emit, disconnect
from anonfiles import socketio as io
from anonfiles.models.room_specs import *
from anonfiles import cache
from anonfiles.errors.handle_all import Halt
from anonfiles.utils.validations import validator


@io.on('try_room', namespace='/user')
def try_room(message):
    room_name = message.get('name')
    room_pass = message.get('pass')
    is_room = cache.get(room_name)
    user = get_user(cache, request.sid)
    user_name = get_user_name(cache, request.sid)
    password = None if (room_name is None) or (is_room is None) else is_room[
        "pass"]
    if is_user_room(cache, room_name, request.sid):
        raise Halt(1011, "user is already in this room")
    if password and room_pass == password:
        join_room(room_name)
        add_user_room(cache, room_name, request.sid)
        emit("joined", {"user": {user: user_name}, "room": room_name},
             to=room_name, include_self=True)
    else:
        raise Halt(1011, "incorrect password")


@io.on('connect', namespace='/user')
@validator
def connection(client):
    user_id = request.sid
    user_name = user_id
    if hasattr(g, 'payload'):
        user_id = g.payload.get('sub')
        user_name = g.payload.get('name')
        add_user(cache, request.sid, user_id, user_name)
        for room in get_rooms(cache, request.sid):
            print(f'joined {room}')
            join_room(room)
    emit('connected_data', {"user_id": user_id, "user_name": user_name})


@io.on('disconnect', namespace='/user')
def disconnection():
    user = get_user(cache, request.sid)
    if is_logged(user, request.sid):
        cache.delete(request.sid)
    else:
        all_rooms = rooms().copy()
        for room in rooms():
            # remove user from room object in db
            remove_user_room(cache, request.sid, room)
            # remove user from cache
            leave_room(room)
        emit('left', {"user": user}, to=all_rooms)


@io.on('make_room', namespace='/user')
def make_room():
    room, password = create_room(cache)
    print(room, password)
    join_room(room)
    add_user_room(cache, room, request.sid, admin=True)
    emit('created', {'room': room, 'password': password})


@io.on('get_rooms', namespace='/user')
def get_all_rooms():
    emit('all_rooms', get_rooms(cache, str(request.sid), default_rooms=rooms()))


@io.on('get_users', namespace='/user')
def get_all_users(data):
    room_name = data["room"]
    users = get_room_users(cache, room_name)
    if users:
        print('users', users)
        emit('all_users', {"users": users})
    else:
        raise Halt(1003, "error processing data")


@io.on('get_room_info', namespace='/user')
def get_room_info(data):
    room_name = data["roomId"]
    room = is_user_room(cache, room_name, request.sid)
    if room:
        emit('room_info', {'room': room})
    else:
        raise Halt(1003, "forbidden")


@io.on('leave', namespace='/user')
def exit_room(data):
    room = data['name']
    leave_room(room)
    emit("left", {'room': room})

