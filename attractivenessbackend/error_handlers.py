from flask import jsonify
import flask
import logging

from facetoolbox.errors import FaceNotFound, ImageTooSmall
from wtforms import ValidationError
from attractivenessbackend import error_status as status
from attractivenessbackend.errors import GenericException

api = flask.Blueprint('api', __name__, url_prefix='')


def translate_exception(message, status_code):
    """Exception translator.

    This function translates an exception to the appropiate format.

    """
    response = jsonify({"message": str(message), "status_code": status_code})
    response.status_code = status_code
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response


@api.errorhandler(GenericException)
def generic_exception_handler(error):
    status_code = getattr(error, "status_code",
                          status.HTTP_500_INTERNAL_SERVER_ERROR)
    return translate_exception(
        message=error.message,
        status_code=status_code,
    )


@api.errorhandler(FaceNotFound)
def face_not_found_exception_handler(error):
    return translate_exception(
        message="Face not found.",
        status_code=status.HTTP_400_BAD_REQUEST,
    )

@api.errorhandler(ImageTooSmall)
def image_too_small_exception_handler(error):
    return translate_exception(
        message="Image too small.",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@api.errorhandler(ValidationError)
def validation_error_handler(error):
    return translate_exception(
        message="Error at loading file.",
        status_code=status.HTTP_400_BAD_REQUEST)


@api.errorhandler(Exception)
def uncontrolled_exception_handler(error):
    return translate_exception(
        message="Internal Server Error.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
