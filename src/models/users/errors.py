
class UserError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotExistsError(UserError):
    # def __init__(self, message):
    #     self.message = message
    pass

class IncorrectPasswordError(UserError):
    # def __init__(self, message):
    #     self.message = message
    pass

class UserAlreadyRegisteredError(UserError):
    pass

class UserEmailInvalidError(UserError):
    pass