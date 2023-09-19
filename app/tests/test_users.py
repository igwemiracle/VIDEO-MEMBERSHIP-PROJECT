import pytest
from app import db
from app.users.models import User


@pytest.fixture(scope='module')
def setup_session():
    # setup
    session = db.get_session()
    yield session
    # teardown
    query = User.objects.filter(email='test@gmail.com')
    if query.count() != 0:
        query.delete()
    session.shutdown()


def test_create_user(setup_session):
    User.create_user(email='test@gmail.com', password='test123')

def test_duplicate_user(setup_session):
    with pytest.raises(Exception):
        User.create_user(email='test@gmail.com',
                        password='test123')

def test_invalid_email(setup_session):
    with pytest.raises(Exception):
        User.create_user(email='test@gmail',
                        password='test123')
        
def test_invalid_password(setup_session):
    query = User.objects.filter(email='test@gmail.com')
    assert query.count() == 1
    user_obj = query.first()
    assert user_obj.verify_password('test123') is True
    assert user_obj.verify_password('test124') is False
