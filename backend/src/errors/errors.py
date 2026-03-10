class Error(Exception):
    message: str

class SessionExpiredError(Error):
    def __init__(self):
        self.message = "session expired"


class SessionNotFoundError(Error):
    def __init__(self):
        self.message = "session not found"

class UserNotFoundError(Error):
    def __init__(self):
        self.message = "user not found"