import unittest
import os
import json
from attractivenessbackend import error_handlers
from attractivenessbackend.app import app
from attractivenessbackend.errors import GenericException

TEST_RESOURCES = os.path.join(os.getcwd(), "facetoolbox", "resources")


class BaseHandlersTesting(unittest.TestCase):
    def assert_response_is_correct(self, resp, expected_error,
                                   expected_message):
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data["message"], expected_message)
        self.assertEqual(data["status_code"], expected_error)
        self.assertEqual(resp.status_code, expected_error)


class TestTranslateException(BaseHandlersTesting):
    def setUp(self):
        self.app_context = app.app_context()

    def test_given_args_response_is_correct(self):
        expected_error_message = "Random Error"
        expected_status_code = 400
        with self.app_context:
            response = error_handlers.translate_exception(expected_error_message,
                                                          expected_status_code)
            self.assert_response_is_correct(response, expected_status_code,
                                            expected_error_message)
            self.assertEqual(response.headers['Access-Control-Allow-Origin'],
                             "*")
            self.assertEqual(response.headers['Access-Control-Allow-Methods'],
                             'POST')


class TestGenericExceptionHandler(BaseHandlersTesting):
    def setUp(self):
        self.app_context = app.app_context()

    def test_given_error_with_status_code_response_is_correct(self):
        expected_error_message = "Random Error"
        expected_status_code = 400
        exception = GenericException(message=expected_error_message,
                                     status_code=expected_status_code)
        with self.app_context:
            response = error_handlers.generic_exception_handler(
                exception)
            self.assert_response_is_correct(response,
                                            expected_status_code,
                                            expected_error_message)

    def test_given_error_without_status_code_response_is_correct(self):
        expected_error_message = "Random Error"
        expected_status_code = 500
        exception = GenericException(message=expected_error_message)
        with self.app_context:
            response = error_handlers.generic_exception_handler(
                exception)
            self.assert_response_is_correct(response,
                                            expected_status_code,
                                            expected_error_message)


class TestHandlers(BaseHandlersTesting):
    def setUp(self):
        self.app_context = app.app_context()
        self.exception = Exception("Random exception")

    def test_face_not_found_exception_handler(self):
        expected_error_message = "Face not found."
        expected_status_code = 400
        with self.app_context:
            response = error_handlers.face_not_found_exception_handler(
                self.exception)
            self.assert_response_is_correct(response,
                                            expected_status_code,
                                            expected_error_message)

    def test_validation_error_handler(self):
        expected_error_message = "Error at loading file."
        expected_status_code = 400
        with self.app_context:
            response = error_handlers.validation_error_handler(
                self.exception)
            self.assert_response_is_correct(response,
                                            expected_status_code,
                                            expected_error_message)

    def test_uncontrolled_exception_handler(self):
        expected_error_message = "Internal Server Error."
        expected_status_code = 500
        with self.app_context:
            response = error_handlers.uncontrolled_exception_handler(
                self.exception)
            self.assert_response_is_correct(response,
                                            expected_status_code,
                                            expected_error_message)


if __name__ == '__main__':
    unittest.main()
