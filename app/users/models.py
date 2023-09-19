import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from . import validators, security


settings = get_settings()

class User(Model):
    __keyspace__ = settings.astradb_keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()


    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"
    
    def set_password(self, pwd, commit=False):
        pwd_hash = security.generate_hash(pwd)
        self.password = pwd_hash
        if commit:
            self.save()
        return True
    
    def verify_password(self, pwd):
        pwd_hash = self.password

        _, verified = security.verify_hash(pwd_hash, pwd)
        return verified

    
    @staticmethod
    def create_user(email, password=None):
        query = User.objects.filter(email=email)
        if query.count() != 0:
            raise Exception("User already has account!")
        valid, msg, email = validators._validate_email(email)
        if not valid:
            raise Exception(f"Invalid email: {msg}")
        obj = User(email=email)
        obj.set_password(password)
        # obj.password = password
        obj.save()
        return obj