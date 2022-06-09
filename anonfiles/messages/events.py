from flask import session, request
from flask_socketio import join_room, leave_room, rooms, emit
from anonfiles import socketio as io
from anonfiles.models.room_specs import create_room
from anonfiles import cache
from anonfiles.errors.handle_all import Halt
from datetime import datetime


@io.on('send_message', namespace='/user')
def send_message(data):
    room = data["room"]
    message = data["message"]
    user = request.sid
    time = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')
    cur = cache.get(room, None)

    if cur:
        messages = cur["messages"]
        new_message = messages.append(
            {
                "message": message,
                "user": user,
                "time": time
            }
        )
        # update room data
        cache.set(room, cur)
        emit('new_message', {"data": new_message}, room=room)
    else:
        raise Halt(1003, "room was not found")


@io.on('get_all_messages', namespace='/user')
def get_messages(data):
    room = data["room"]
    cur = cache.get(room, None)
    if not cur:
        raise Halt(1003, "room does not exist")
    else:
        users = cur["users"]

        if str(request.sid) in users:
            return emit('all_messages', cur["messages"])

    raise Halt(1003, "unknown error in handler")
