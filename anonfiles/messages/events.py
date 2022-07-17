from flask import session, request, g
from flask_socketio import join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room, get_user, \
    get_user_name, is_user_room, add_message
from anonfiles import cache
from anonfiles.errors.handle_all import Halt
from datetime import datetime


@io.on('send_message', namespace='/user')
def send_message(data):
    room = data["room"]
    message = data["message"]
    new_message = add_message(cache, request.sid, room, message)
    if new_message:
        emit('new_message', {"data": new_message}, to=room, include_self=False)
    else:
        raise Halt(1003, "room was not found")


@io.on('send_file', namespace='/user')
def send_file(data):
    print('\n\n\nin send file', type(data["files"]))
    files = data["files"]
    room = data["room"]
    file_names = ''.join([f"{index+1}.{file['name']}\n" for index, file in enumerate(files)])
    # ensure user has access to this room
    if is_user_room(cache, room, request.sid):
        print('sending files to client')
        add_message(
            cache,
            request.sid,
            room,
            file_names
        )
        emit('received_files', {"files": files}, to=room, include_self=False)


@io.on('get_all_messages', namespace='/user')
def get_messages(data):
    room = data["room"]
    cur = cache.get(room)
    print('getting messages in messages endpoint')
    if not cur:
        raise Halt(1003, "room does not exist")
    else:
        if is_user_room(cache, room, request.sid):
            return cur["messages"]

    raise Halt(1003, "unknown error in handler")
