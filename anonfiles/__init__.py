#init
from flask_session import Session
from flask_caching import Cache
from flask_socketio import SocketIO
from authlib.integrations.flask_client import OAuth
sess = Session()
cache = Cache()
socketio = SocketIO()
auth = OAuth()




