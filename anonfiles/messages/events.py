from flask import session, request, g
from flask_socketio import join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room, get_user, get_user_name
from anonfiles import cache
from anonfiles.errors.handle_all import Halt
from datetime import datetime


@io.on('send_message', namespace='/user')
def send_message(data):
    room = data["room"]
    message = data["message"]
    user = get_user_name(cache, rid=request.sid)
    time = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    cur = cache.get(room)
    print(f'message received: {message}, room: {cur}')
    if cur:
        messages = cur["messages"]
        new_message = {
                "message": message,
                "user": user,
                "time": time,
                "user_id": get_user(cache, request.sid)
            }
        messages.append(
            new_message
        )

        # update room data
        cache.set(room, cur)
        print('emitting new message')
        emit('new_message', {"data": new_message}, to=room, include_self=False)
    else:
        raise Halt(1003, "room was not found")


@io.on('get_all_messages', namespace='/user')
def get_messages(data):
    room = data["room"]
    cur = cache.get(room)
    user = get_user(cache, request.sid)
    print('getting messages in messages endpoint')
    if not cur:
        raise Halt(1003, "room does not exist")
    else:
        users = cur["users"]
        print(users)
        if str(request.sid) or user in users:
            return emit('all_messages', cur["messages"], to=request.sid)

    raise Halt(1003, "unknown error in handler")
