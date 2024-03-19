from app import app


def init_app():
    global app
    return app


app = init_app()
if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")
