from anonfiles.app import make_app, socketio


app = make_app()

if __name__ == "__main__":
    socketio.init_app(app, cors_allowed_origins=[])
    socketio.run(app, host="0.0.0.0", port=8011)
