#init
from flask_session import Session
from flask_caching import Cache
from flask_socketio import SocketIO
sess = Session()
cache = Cache()
socketio = SocketIO()



