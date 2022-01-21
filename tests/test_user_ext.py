import pytest
from gyguesssong.user.ext import user_ext, current_user
from gyguesssong.user.model import User


@pytest.fixture
def sample_user_model():
    return User("sample_id", "GYCHEN")


@pytest.fixture
def sample_user_dict(sample_user_model):
    return {
        "id": sample_user_model.id,
        "name": sample_user_model.name
    }


@pytest.fixture
def sample_user_jwt_token(sample_user_dict):
    return user_ext._encode_jwt_token(sample_user_dict)


def test_authorize_redirect(app):
    redirect_uri = 'https://local.gyhost.icu/login/redirect'
    with app.test_request_context('/login'):
        response = user_ext.authorize_redirect(redirect_uri)
        assert response.status_code == 302
        assert response.headers['location'].startswith('https://accounts.google.com')


def test_jwt(app, sample_user_dict):
    encoded = user_ext._encode_jwt_token(sample_user_dict)
    assert user_ext._decode_jwt_token(encoded) == sample_user_dict


def test_current_user(app, sample_user_jwt_token, sample_user_model):
    headers = {
        'Authorization': f'Bearer {sample_user_jwt_token}'
    }
    with app.test_request_context("/", headers=headers):
        assert current_user.id == sample_user_model.id
        assert current_user.name == sample_user_model.name
