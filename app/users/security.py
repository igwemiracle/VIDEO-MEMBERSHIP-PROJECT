from argon2 import PasswordHasher

def generate_hash(plain_pwd):
    pwdhash = PasswordHasher()
    return pwdhash.hash(plain_pwd)


def verify_hash(pwd_hash, plain_pwd):
    pwdhash = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = pwdhash.verify(pwd_hash, plain_pwd)
    except:
        pass
