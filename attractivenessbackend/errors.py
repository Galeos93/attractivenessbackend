class GenericException(Exception):

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)

        if message is None:
            message = "Sorry, an error occurred..."

        self.message = message

        if status_code is not None:
            self.status_code = status_code
        self.payload = payload