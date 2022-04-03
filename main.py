from flask import Flask, request
from flask_session import Session
from flask_socketio import SocketIO, join_room, leave_room, send
from config.init_config import init_config
from flask_caching import Cache
from anonfiles.models.generate_pass import generate_pass

app = Flask(__name__)

get_config = init_config()
app.config.from_object(get_config)

io = SocketIO(app)

sess = Session()
cache = Cache(app)

sess.init_app(app)


@app.route("/")
def create_room():
    room_pass = generate_pass()
    # cache room_name:password
    return room_pass


@io.on('join', namespace='/room')
def join_room(data):
    print(data)
    #user = session['username']
    room = data['room']
    join_room(room)
    #send(user, to=room)


if __name__ == "__main__":
    io.run(app, host="127.0.0.1", port=8080, threading=True)
    #app.run()


