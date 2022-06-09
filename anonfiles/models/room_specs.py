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
        "users": []
    }
    cache.set(room_name, room)

    return room_name, room_pass


def add_user(cache, room: str, user: str):
    cur = cache.get(room, None)

    if not cur:
        raise Halt(1003, 'room does not exist')
    else:
        users = cur["users"]
        users.append(user)
        cache.set(room, cur)

