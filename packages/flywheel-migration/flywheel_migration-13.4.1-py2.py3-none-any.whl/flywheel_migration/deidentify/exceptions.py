"""Provides validation error for deid templates"""


class ValidationError(Exception):
    """Indicates that the profile is invalid.

    Attributes:
        path (str): The path to the deid profile
        errors (list(str)): The list of error messages
    """

    def __init__(self, path, errors):
        super(ValidationError, self).__init__()
        self.path = path
        self.errors = errors

    def __str__(self):
        result = "The profile at {} is invalid:".format(self.path)
        for error in self.errors:
            result += "\n  {}".format(error)
        return result
