from . import (
    CWD,
    EXHIBITION_DIR,
    EXHIBITION_PAINTINGS_DIR,
    PAINTING_DIR,
    PROFILE_DIR,
    UPLOAD_DIR,
)
from werkzeug.utils import secure_filename
import logging
import os
import shutil


def init_directories():
    os.chdir(CWD)
    try:
        os.mkdir("uploads")
        os.chdir(os.path.join(CWD, "uploads"))
        os.mkdir("exhibitions")
        os.mkdir("exhibition_painting")
        os.mkdir("paintings")
        os.mkdir("profiles")
    except FileExistsError:
        pass
    except OSError as error:
        logging.error(str(error))
    finally:
        os.chdir(CWD)


############################ EXHIBITION FILE MANAGEMENT BLOCK


def create_exhibition_painting_dir(dir_name):
    os.chdir(EXHIBITION_PAINTINGS_DIR)
    os.mkdir(dir_name)
    os.chdir(CWD)


def delete_exhibition_painting_dir(dir_name):
    shutil.rmtree(os.path.join(EXHIBITION_PAINTINGS_DIR, dir_name))


def save_exhibition_banner_file(file):
    file.save(os.path.join(EXHIBITION_DIR, secure_filename(file.filename)))


def delete_exhibition_banner_file(filename):
    path, filename = os.path.split(filename)
    os.remove(os.path.join(EXHIBITION_DIR, secure_filename(filename)))


def get_exhibition_banner_path(filename):
    return os.path.join(EXHIBITION_DIR, secure_filename(filename))


def rename_exhibition_folder_name(oldname, newname):
    os.chdir(EXHIBITION_PAINTINGS_DIR)
    os.rename(
        f"{oldname}",
        f"{newname}",
    )
    os.chdir(CWD)


############################ END OF EXHIBITION FILE MANAGEMENT BLOCK


############################ EXHIBITION PAINTING FILE MANAGEMENT BLOCK


def add_painting_file(dirname, image, audio):
    path = os.path.join(EXHIBITION_PAINTINGS_DIR, dirname)
    os.chdir(path)
    image["file"].save(os.path.join(path, secure_filename(image["filename"])))
    audio["file"].save(os.path.join(path, secure_filename(audio["filename"])))
    os.chdir(CWD)


def get_painting_file_path(dir_name, filename):
    return os.path.join(
        os.path.join(EXHIBITION_PAINTINGS_DIR, dir_name), secure_filename(filename)
    )


############################ END OF EXHIBITION PAINTING FILE MANAGEMENT BLOCK


############################ USER PAINTING FILE MANAGEMENT BLOCK


def add_user_painting_file(file, filename):
    file.save(os.path.join(PAINTING_DIR, secure_filename(filename)))


def get_user_painting_file_path(filename):
    return os.path.join(PAINTING_DIR, secure_filename(filename))


def delete_user_painting_file(filename):
    path, filename = os.path.split(filename)
    os.remove(os.path.join(PAINTING_DIR, secure_filename(filename)))


############################ END OF USER PAINTING FILE MANAGEMENT BLOCK


############################ USER_PROFILE FILE MANAGEMENT BLOCK
def add_user_profile_file(file, filename):
    file.save(os.path.join(PROFILE_DIR, secure_filename(filename)))


def get_user_profile_file_path(filename):
    return os.path.join(PROFILE_DIR, secure_filename(filename))


def delete_user_profile_file(filename):
    path, filename = os.path.split(filename)
    os.remove(os.path.join(PROFILE_DIR, secure_filename(filename)))


############################ END OF USER_PROFILE FILE MANAGEMENT BLOCK


def create_exhibition_dir(dir_name):
    os.chdir(EXHIBITION_DIR)
    os.mkdir(dir_name)
    os.chdir(CWD)


def create_file(
    handler,
):
    handler(UPLOAD_DIR)


def delete_dir_and_files(path: str):
    shutil.rmtree(path)
