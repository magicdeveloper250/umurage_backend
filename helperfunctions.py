import cryptocode
from typing import OrderedDict


KEY = "12345678"


def convertToObject(keys, values):
    my_objects = []
    for i in range(len(values)):
        object = {}
        for j in range(len(values[i])):
            object[keys[j]] = values[i][j]
        my_objects.append(object)
    return my_objects


def authorize(user_id, auth_key, session_id, session_key) -> bool:
    """checking if user who is trying to access api is eligible to do so."""
    import flask

    print(flask.session.get("user_id"))
    user_id = cryptocode.decrypt(user_id, password=KEY)
    auth_key = cryptocode.decrypt(auth_key, password=KEY)

    # comparing auths from client with auths that saved in current user session
    return user_id == session_id and auth_key == session_key


def generate_mime(extension):
    image = (".png", ".jpg", ".jpeg")
    audio = (".mp3", ".ma4", ".wav")
    if extension in image:
        return f"image/{extension}".replace(".", "")
    elif extension in audio:
        return f"audio/{extension}".replace(".", "")
    return None
