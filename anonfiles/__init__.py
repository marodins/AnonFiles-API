#init
from flask_session import Session
from flask_caching import Cache
from flask_socketio import SocketIO
from authlib.integrations.flask_client import OAuth
from config.config import Config
sess = Session()
cache = Cache()
socketio = SocketIO(max_http_buffer_size=10**8)
auth = OAuth()
auth.register(
    'auth0',
    client_id=Config.AUTH0_CLIENT_ID,
    client_secret=Config.AUTH0_CLIENT_SECRET,
    api_base_url=Config.AUTH0_API_BASE_URL,
    authorize_url=f'{Config.AUTH0_API_BASE_URL}/authorize',
    access_token_url=f'{Config.AUTH0_ACCESS_TOKEN_URL}',
    server_metadata_url=Config.AUTH0_SERVER_METADATA_URL,
    client_kwargs={
        "scope": "openid profile email"
    }

)



