from passlib.hash import pbkdf2_sha512
import re

class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_id_match = re.compile('^[\w-]+@([\w-]+\.)+[\w]$')
        return True if email_id_match.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes password using pbkdf2_sha512
        :param password: The sha512 password from login/user form
        :return: sha512 -> pbkdf2_sha512 password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        checks the password given by user matches DB's. The DB password is encrypted.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if match, False if otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)