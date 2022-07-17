import random
from datetime import datetime
from string import digits, ascii_letters
from hashlib import md5
from random import getrandbits
from anonfiles.errors.handle_all import Halt


def generate_pass():
    return md5(str(getrandbits(10)).encode()).hexdigest()


def generate_name():
    return ''.join(random.choices(digits+ascii_letters, k=15))


def create_room(cache):
    room_pass = generate_pass()
    room_name = generate_name()

    while cache.get(room_name) is not None:
        room_name = generate_name()
    room = {
        "pass": room_pass,
        "messages": [],
        "users": [],
        "admin": []
    }
    cache.set(room_name, room)

    return room_name, room_pass


def add_user(cache, temp_id, main_id, uname=None):
    # associate current session with auth id
    cache.set(temp_id, main_id)
    # create completely new user id associated with empty list instance
    if not cache.get(main_id):
        cache.set(main_id, {'rooms': list(), 'name': uname})


def get_rooms(cache, rid, default_rooms=None):
    user = get_user(cache, rid)
    # same id as request id not a registered user
    if not is_logged(user, rid):
        return default_rooms
    else:
        return cache.get(user)['rooms']


def is_user_room(cache, room_name, rid):
    room = cache.get(room_name)
    user = get_user(cache, rid)
    if room:
        for person in room['users']:
            if person.get(user):
                return room


def get_room_users(cache, room_name):
    room = cache.get(room_name)
    return room if not room else room["users"]


def get_user(cache, req_id):
    user = cache.get(req_id)
    return user if user else req_id


def get_user_name(cache, rid):
    """ returns user's name if user is logged in otherwise rid """
    uid = get_user(cache, str(rid))
    # anonymous user, no name stored
    if not is_logged(uid, str(rid)):
        return rid
    return cache.get(uid)['name']


def is_logged(uid, rid):
    return uid != rid


def add_user_room(cache, room: str, rid: str, admin=False):
    cur = cache.get(room)
    user = get_user(cache, rid)
    user_name = get_user_name(cache, rid)
    if not cur:
        raise Halt(1003, 'room does not exist')

    if is_logged(rid, user):
        cur_user = cache.get(user)
        cur_user['rooms'].append(room)
        cache.set(user, cur_user)

    if admin:
        cur["admin"] = [user, user_name]

    users = cur["users"]
    users.append({user: user_name})
    cache.set(room, cur)


def remove_user_room(cache, rid, room_name):
    room = cache.get(room_name)
    if room:
        users = room["users"]
        for index, ob in enumerate(users):
            if ob.get(rid):
                users.pop(index)
                break
        cache.set(room_name, room)


def add_message(cache, rid, room, message):
    user = get_user_name(cache, rid=rid)
    time = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    cur = cache.get(room)
    print(f'message received: {message}, room: {cur}')
    if cur:
        messages = cur["messages"]
        new_message = {
            "message": message,
            "user": user,
            "time": time,
            "user_id": get_user(cache, rid)
        }
        messages.append(
            new_message
        )

        # update room data
        cache.set(room, cur)
        print('emitting new message')
        return new_message

