from dotenv import load_dotenv

load_dotenv()
import cloudinary
import cloudinary.uploader
import cloudinary.api
import uuid
import datetime
import cryptocode
from auth import EXHIBITION_PAINTINGS_KEY
from werkzeug.utils import secure_filename
import threading
import os

config = cloudinary.config(secure=True)


############################ CLOUDINARY FILE MANAGEMENT BLOCK
def process_audio_file(f, public_id):
    f.save(dst=os.path.join(os.getcwd(), f.name))
    with open(f.name, "rb") as f:
        res = cloudinary.uploader.upload_large(
            f,
            public_id=public_id,
            unique_filename=True,
            resource_type="video",
        )
        return res["secure_url"]


def add_painting_file(file_owner, image, audio):
    IMAGE_PUBLIC_ID = (
        file_owner
        + str(uuid.uuid4())
        + str(datetime.datetime.now()).replace(" ", "_").lower()
    )
    AUDIO_PUBLIC_ID = (
        file_owner
        + str(uuid.uuid4())
        + str(datetime.datetime.now()).replace(" ", "_").lower()
    )
    image_thread = threading.Thread(
        daemon=True,
        target=lambda: cloudinary.uploader.upload(
            image,
            public_id=IMAGE_PUBLIC_ID,
            unique_filename=True,
        ),
    )
    audio_thread = threading.Thread(
        target=lambda: process_audio_file(audio, AUDIO_PUBLIC_ID), daemon=True
    )
    audio_url = cloudinary.CloudinaryImage(AUDIO_PUBLIC_ID).build_url()

    image_url = cloudinary.CloudinaryImage(IMAGE_PUBLIC_ID).build_url()

    image_thread.start()
    audio_thread.start()
    return (image_url, audio_url)


def get_exhibition_painting_file(encrypted_path: str):

    path = encrypted_path.replace(" ", "+")
    decrypted_path = cryptocode.decrypt(path, EXHIBITION_PAINTINGS_KEY)
    return decrypted_path


def add_user_painting_file(image_file, image_owner):

    PUBLIC_ID = (
        image_owner
        + str(uuid.uuid4())
        + str(datetime.datetime.now()).replace(" ", "_").lower()
    )
    upload_thread = threading.Thread(
        target=lambda: cloudinary.uploader.upload(
            image_file,
            public_id=PUBLIC_ID,
            unique_filename=True,
            overwrite=True,
        )
    )
    image_url = cloudinary.CloudinaryImage(PUBLIC_ID).build_url()
    upload_thread.start()
    return image_url


def save_exhibition_banner_file(image_file, image_owner):

    PUBLIC_ID = (
        image_owner
        + str(uuid.uuid4())
        + str(datetime.datetime.now()).replace(" ", "_").lower()
    )
    upload_thread = threading.Thread(
        target=lambda: cloudinary.uploader.upload(
            image_file,
            public_id=PUBLIC_ID,
            unique_filename=True,
            overwrite=True,
        )
    )
    image_url = cloudinary.CloudinaryImage(PUBLIC_ID).build_url()
    # upload_thread.start()
    return image_url


def add_user_profile_file(image_file, image_owner):

    PUBLIC_ID = (
        image_owner
        + str(uuid.uuid4())
        + str(datetime.datetime.now()).replace(" ", "_").lower()
    )
    upload_thread = threading.Thread(
        target=lambda: cloudinary.uploader.upload(
            image_file,
            public_id=PUBLIC_ID,
            unique_filename=True,
            overwrite=True,
        )
    )
    image_url = cloudinary.CloudinaryImage(PUBLIC_ID).build_url()
    upload_thread.start()
    return image_url


############################  NATIVE OPERATING SYSTEM  FILE MANAGEMENT BLOCK


# def create_exhibition_dir(dir_name):
#     os.chdir(EXHIBITION_DIR)
#     os.mkdir(dir_name)
#     os.chdir(CWD)


# def create_file(
#     handler,
# ):
#     handler(UPLOAD_DIR)


# def delete_dir_and_files(path: str):
#     shutil.rmtree(path)


# def init_directories():
#     os.chdir(CWD)
#     try:
#         os.mkdir("uploads")
#         os.chdir(os.path.join(CWD, "uploads"))
#         os.mkdir("exhibitions")
#         os.mkdir("exhibition_painting")
#         os.mkdir("paintings")
#         os.mkdir("profiles")
#     except FileExistsError:
#         pass
#     except OSError as error:
#         logging.error(str(error))
#     finally:
#         os.chdir(CWD)


############################ EXHIBITION FILE MANAGEMENT BLOCK


# def create_exhibition_painting_dir(dir_name):
#     os.chdir(EXHIBITION_PAINTINGS_DIR)
#     os.mkdir(dir_name)
#     os.chdir(CWD)


# def delete_exhibition_painting_dir(dir_name):
#     shutil.rmtree(os.path.join(EXHIBITION_PAINTINGS_DIR, dir_name))


# def delete_exhibition_banner_file(filename):
#     path, filename = os.path.split(filename)
#     os.remove(os.path.join(EXHIBITION_DIR, secure_filename(filename)))


# def get_exhibition_banner_path(filename):
#     return os.path.join(EXHIBITION_DIR, secure_filename(filename))


# def rename_exhibition_folder_name(oldname, newname):
#     os.chdir(EXHIBITION_PAINTINGS_DIR)
#     os.rename(
#         f"{oldname}",
#         f"{newname}",
#     )
#     os.chdir(CWD)


# def get_user_painting_file_path(filename):
#     return os.path.join(PAINTING_DIR, secure_filename(filename))


# def delete_user_painting_file(filename):
#     path, filename = os.path.split(filename)
#     os.remove(os.path.join(PAINTING_DIR, secure_filename(filename)))


# def get_user_profile_file_path(filename):
#     return os.path.join(PROFILE_DIR, secure_filename(filename))


# def delete_user_profile_file(filename):
#     path, filename = os.path.split(filename)
#     os.remove(os.path.join(PROFILE_DIR, secure_filename(filename)))
