from app import app
from filemanagement.filemanager import init_directories


app = app
if __name__ == "__main__":
    init_directories()

    app.run(debug=True, host="0.0.0.0")
