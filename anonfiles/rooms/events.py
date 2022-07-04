from flask import request, g
from flask_socketio import join_room, leave_room, rooms, emit, disconnect
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room, add_user, \
    add_user_room, get_rooms, is_logged, get_user, get_user_name, \
    remove_user_room, get_room_users
from anonfiles import cache
from anonfiles.errors.handle_all import Halt
from anonfiles.utils.validations import validator


@io.on('try_room', namespace='/user')
def try_room(message):
    print('in try_room')
    room_name = message.get('name')
    room_pass = message.get('pass')
    print('received serverside name and pass', room_name, room_pass)
    is_room = cache.get(room_name)
    print(is_room)
    user = get_user(cache, request.sid)
    print('user is', user)
    password = None if (room_name is None) or (is_room is None) else is_room[
        "pass"]
    print(room_name, password, is_room)
    if user in is_room["users"]:
        raise Halt(1011, "user is already in this room")
    if password and room_pass == password:
        join_room(room_name)
        add_user_room(cache, room_name, request.sid)
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
    if hasattr(g, 'payload'):
        user_id = g.payload.get('sub')
        user_name = g.payload.get('name')
        print('in payload')
        add_user(cache, request.sid, user_id, user_name)
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
        emit('left', {"user": request.sid}, to=all_rooms)


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
        emit('all_users', {"users": users}, to=room_name)
    else:
        raise Halt(1003, "error processing data")


@io.on('leave', namespace='/user')
def exit_room(data):
    room = data['name']
    leave_room(room)
    emit("left", {'room': room})

