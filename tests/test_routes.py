import unittest
import os
import base64
from unittest.mock import MagicMock, patch

TEST_RESOURCES = os.path.join(os.getcwd(), "facetoolbox", "resources")

"""
A good response includes the appropiate headers
I should check how to allow only the server to make requests.
I should check image format
"""

import attractivenessbackend.app as srv
import io
import json


class TestWrongRoute(unittest.TestCase):
    ERROR_404 = ("404 Not Found: The requested URL was not found on the "
                 "server. If you entered the URL manually please check your "
                 "spelling and try again.")

    def setUp(self):
        srv.app.config['TESTING'] = True
        self.app = srv.app.test_client()

    def assert_error_response(self, resp, status_code=500, message=""):
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data["message"], message)
        self.assertEqual(resp.status_code, status_code)

    def test_given_wrong_route_response_is_correct(self):
        data = {'file': (io.BytesIO(b"random_string"), 'filename.png')}
        resp = self.app.post('/save_images', data=data)
        self.assert_error_response(resp, status_code=404,
                                   message=self.ERROR_404)


class TestSaveImage(unittest.TestCase):
    def setUp(self):
        srv.app.config['TESTING'] = True
        self.app = srv.app.test_client()
        self.sample_image_path = os.path.join(TEST_RESOURCES, "frontal_face")

    def assert_error_response(self, resp, status_code=500, message=""):
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data["message"], message)
        self.assertEqual(resp.status_code, status_code)

    def test_given_no_file_error_is_controlled(self):
        data = {}
        resp = self.app.post('/attractiveness/rate', data=data)
        self.assert_error_response(resp, status_code=400,
                                   message="Error at loading file.")

    def test_given_not_image_error_is_controlled(self):
        data = {'file': (io.BytesIO(b"random_string"), 'filename.png')}
        resp = self.app.post('/attractiveness/rate', data=data)
        self.assert_error_response(resp, status_code=400,
                                   message="Error at loading image.")

    def test_given_face_image_response_is_correct(self):
        with open(self.sample_image_path, "rb") as f_hdl:
            data = {'file': (io.BytesIO(f_hdl.read()), 'filename.png')}
        resp = self.app.post('/attractiveness/rate', data=data)
        data = json.loads(resp.get_data(as_text=True))
        base64.decodebytes(bytes(data["image"], "ascii"))
        self.assertEqual(data["score"], 3.83)
        self.assertEqual(resp.status_code, 200)

    def test_given_noface_image_response_is_correct(self):
        noface_image = os.path.join(TEST_RESOURCES, "black_image.jpg")
        with open(noface_image, "rb") as f_hdl:
            data = {'file': (io.BytesIO(f_hdl.read()), 'filename.png')}
        resp = self.app.post('/attractiveness/rate', data=data)
        self.assert_error_response(resp, status_code=400,
                                   message="Face not found.")

    def test_given_small_image_response_is_correct(self):
        noface_image = os.path.join(TEST_RESOURCES, "tiny_image.jpg")
        with open(noface_image, "rb") as f_hdl:
            data = {'file': (io.BytesIO(f_hdl.read()), 'filename.png')}
        resp = self.app.post('/attractiveness/rate', data=data)
        self.assert_error_response(resp, status_code=400,
                                   message="Image too small.")

    @patch("attractivenessbackend.routes.face_locator")
    def test_given_uncontrolled_exception_response_is_correct(
            self, face_locator_mock):
        face_extractor_mock = MagicMock()
        face_locator_mock.extract_face = face_extractor_mock
        face_extractor_mock.side_effect = Exception("Random Exception")
        with open(self.sample_image_path, "rb") as f_hdl:
            data = {'file': (io.BytesIO(f_hdl.read()), 'filename.png')}
        resp = self.app.post('/attractiveness/rate', data=data)
        self.assert_error_response(resp, status_code=500,
                                   message="Internal Server Error.")

    def test_given_wrong_filename_validation_error_is_raised(self):
        with open(self.sample_image_path, "rb") as f_hdl:
            data = {'file': (io.BytesIO(f_hdl.read()), 'filme.jpg')}
        resp = self.app.post('/attractiveness/rate', data=data)
        self.assert_error_response(resp, status_code=400,
                                   message="Error at loading file.")


if __name__ == '__main__':
    unittest.main()
