import secrets
import os
from flask import current_app
from PIL import Image


def uploadImage(image, path=''):
    random_ex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image.filename)
    filename = random_ex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/' + path, filename)

    size = (1200,840)
    im = Image.open(image)
    im.thumbnail(size)
    im.save(image_path)

    return path + filename
