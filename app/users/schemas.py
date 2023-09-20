from pydantic import BaseModel, validator, EmailStr, SecretStr
from app.users.models import User

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr

class UserSignUpSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    @validator("email")
    def email_avaliable(cls, v, values, **kwargs):
        query = User.objects.filter(email=v)
        if query.count() != 0:
            raise ValueError("The email you entered is not avaliable")
        return v

    @validator("confirm_password")
    def password_match(cls, v, values, **kwargs):
        password = values.get('password')
        if password is None:
            raise ValueError("Password is missing")
        confirm_password = v
        if password != confirm_password:
            raise ValueError('Passwords do not match!')
        return v

