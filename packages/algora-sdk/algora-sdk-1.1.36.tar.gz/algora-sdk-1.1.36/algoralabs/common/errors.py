class CustomBaseException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return self.msg


class AuthenticationError(CustomBaseException):
    """
    Custom exception for authentication errors when interacting with the APIs
    """

    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg)


class ApiError(CustomBaseException):
    """
    Custom exception for non authentication related errors
    """

    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg)


class InvalidConfig(CustomBaseException):
    """
    Custom exception for request missing required fields
    """

    def __init__(self, message: str):
        super().__init__(message)


class CastingError(CustomBaseException):
    """
    Custom exception for request missing required fields
    """

    def __init__(self, message: str):
        super().__init__(message)


class InvalidRequest(CustomBaseException):
    """
    Custom exception for request missing required fields
    """

    def __init__(self, message: str):
        super().__init__(message)
