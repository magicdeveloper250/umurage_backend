from app import app
from filemanagement.filemanager import init_directories


def init_app():
    global app
    init_directories()
    return app


app = init_app()
if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")
