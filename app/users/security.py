from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError 

def generate_hash(plain_pwd):
    pwdhash = PasswordHasher()
    return pwdhash.hash(plain_pwd)


def verify_hash(pwd_hash, plain_pwd):
    pwdhash = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = pwdhash.verify(pwd_hash, plain_pwd)
    except VerifyMismatchError:
        verified = False
        msg = f"Invalid password."
    except Exception as e:
        verified = False
        msg = f"Unexpected error \n{e}"
    return msg, verified
