import unittest
import os
import json
from attractivenessbackend.app import handle_404
from attractivenessbackend.app import app

TEST_RESOURCES = os.path.join(os.getcwd(), "facetoolbox", "resources")


class TestHandle404(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()

    def test_given_wrong_error_correct_response_is_returned(self):
        error_message = "Random Error"
        with self.app_context:
            response, status_code = handle_404(Exception(error_message))
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data["message"], error_message)
            self.assertEqual(data["error"], 404)
            self.assertEqual(status_code, 404)


if __name__ == '__main__':
    unittest.main()
