from builtins import Exception


class InputError(Exception):
    def __init__(self, error_message):
        self.response = 'An input error has occurred: ' + error_message
        super(InputError, self).__init__(self.response)


class FileExtensionError(Exception):
    def __init__(self, ext):
        self.response = 'Incorrect file extension.  .' + ext + ' is required'
        super(FileExtensionError, self).__init__(self.response)
