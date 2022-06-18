import numpy as np
import logging
import psutil
from flask import jsonify, request, make_response
import io
import os
import base64
from PIL import Image, ImageOps
from facetoolbox.apps import (inference, face_locator)
from facetoolbox.errors import FaceNotFound, ImageTooSmall
from attractivenessbackend.error_handlers import api, GenericException
from attractivenessbackend.forms import UploadForm

CONFIG = os.getenv("CONFIG", os.path.join(os.getcwd(),
                                          "resources", "config.yaml"))
MODEL = inference.load_model(CONFIG)


@api.route('/attractiveness/rate', methods=['POST'])
def attractiveness_rate():
    form = UploadForm(request.files)
    form.validate_file(form.file)
    image_filestorage = form.file.data
    try:
        image = Image.open(image_filestorage)
        image = ImageOps.exif_transpose(image)
    except Exception:
        raise GenericException(message="Error at loading image.",
                               status_code=400)
    rgb_image = image.convert("RGB")
    rgb_image.thumbnail((1000, 1000))
    try:
        cropped_rgb_array = face_locator.extract_face(rgb_image, config=CONFIG)
    except FaceNotFound:
        raise FaceNotFound
    except ImageTooSmall:
        raise ImageTooSmall
    else:
        pass

    score = inference.classify_face(cropped_rgb_array, MODEL)

    buffer_full_image = io.BytesIO()
    rgb_image.save(buffer_full_image, format="JPEG")
    encoded_string = base64.b64encode(buffer_full_image.getvalue()).decode()

    json_response = jsonify(
        dict(image=encoded_string, score=np.round(score, 2)))
    resp = make_response(json_response)
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST'

    return resp
