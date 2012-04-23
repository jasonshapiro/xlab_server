class NewPhoneException(Exception):
    """
    Raised when a user tries to login on a second phone. A user account can only
    be associated with one phone at a time.
    """
    pass

class InactivePhoneException(Exception):
    """
    Raised when a phone makes an API call, but we find that the device is no
    longer active in association with the user account making the API call.
    """
    pass

class InvalidDataException(Exception):
    """
    Raised when a phone makes an API call with data in an invalid format.
    """
    pass
