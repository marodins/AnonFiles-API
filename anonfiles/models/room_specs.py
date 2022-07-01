import random
import time
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
        "admin": ''
    }
    cache.set(room_name, room)

    return room_name, room_pass


def add_user(cache, temp_id, main_id, uname):
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


def get_user(cache, req_id):
    user = cache.get(req_id)
    print('user', user, cache.get(user))
    return user if user else req_id


def get_user_name(cache, rid=None, uid=None):
    """ requires either uid or rid argument """
    if rid:
        uid = get_user(cache, rid)
    # anonymous user, no name stored
    if not is_logged(uid, rid):
        return rid
    return cache.get(uid)['name']


def is_logged(uid, rid):
    return uid != rid


def add_user_room(cache, room: str, user: str, admin=False, logged_in=False):
    cur = cache.get(room)
    if not cur:
        raise Halt(1003, 'room does not exist')

    if logged_in:
        cur_rooms = cache.get(user)
        cur_rooms['rooms'].append(room)
        cache.set(user, cur_rooms)

    if admin:
        cur["admin"] = user

    users = cur["users"]
    users.append(get_user_name(cache, user=user))
    cache.set(room, cur)

