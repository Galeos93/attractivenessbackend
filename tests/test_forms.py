"""Module for testing forms."""

import unittest
import cv2


def build_image_b64_str(image):
    return cv2.imencode('.jpg', image)[1].tostring().encode('base64')


class TestUploadForm(unittest.TestCase):
    """Class that tests the utilities provided by UploadForm"""
    def setUp(self):
        pass

    def test_given_correct_input_validation_is_correct(self):
        pass

    def test_given_no_file_validate_file_method_raises_validation_error(self):
        pass

    def test_wrong_filename_validate_file_method_raises_validation_error(self):
        pass


if __name__ == '__main__':
    unittest.main()