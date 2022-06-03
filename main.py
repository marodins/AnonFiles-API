from anonfiles.app import make_app, socketio


app = make_app()

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8080)


