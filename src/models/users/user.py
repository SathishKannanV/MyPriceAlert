import uuid

from src.common.database import Database
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.common.utils import Utils
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def login_valid(email, password):
        """
        This verifies user email and password (sent by site forms) is valid or not
        :param email: The User's Email
        :param password: A sha512 hashed password
        :return: True if valid and False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email}) # password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell user email is not registered
            raise UserErrors.UserNotExistsError("Your user does not exists")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell user password is wrong
                raise UserErrors.IncorrectPasswordError("Your password was wrong")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method register using email and password submitted. Password is sha512 hashed.
        :param email: user email. (can be invalid as well)
        :param password: sha512 hashed password
        :return: True if successful, False otherwise. Exception also can be raised.
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            # Tell user that email id is already taken.
            raise UserErrors.UserAlreadyRegisteredError("The e-mail id used to register already exists")
        if not Utils.email_is_valid:
            # Tell user that email is not constructed properly
            raise UserErrors.UserEmailInvalidError("The e-mail id submitted is not valid email")

        User(email, Utils.hash_password(password)).save_to_mongo()

        return True

    def save_to_mongo(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(** Database.find_one(UserConstants.COLLECTION, {"email": email}))

    def get_alerts(self):
        return Alert.find_by_email(self.email)