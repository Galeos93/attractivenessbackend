import unittest
from attractivenessbackend import errors


class TestHandle404(unittest.TestCase):
    def assert_generic_exception_attributes(self, instance, message,
                                            status_code, payload):
        self.assertEqual(instance.message, message)
        self.assertEqual(getattr(instance, "status_code", None), status_code)
        self.assertEqual(instance.payload, payload)

    def test_given_set_of_parameters_instance_is_correct(self):
        input_parameters = (
            dict(message="foo", status_code=404, payload="bar"),
            dict(status_code=404, payload="bar"),
            dict(payload="bar")
        )

        expected_parameters = (("foo", 404, "bar"),
                               ("Sorry, an error occurred...", 404, "bar"),
                               ("Sorry, an error occurred...", None, "bar"))
        for input_params, expected_params in zip(input_parameters,
                                                 expected_parameters):
            error_instance = errors.GenericException(**input_params)
            self.assert_generic_exception_attributes(error_instance,
                                                     *expected_params)


if __name__ == '__main__':
    unittest.main()
