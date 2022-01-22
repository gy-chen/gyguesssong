import json
from functools import wraps
from flask import request, abort, current_app
from werkzeug.local import LocalProxy
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from authlib.jose.util import extract_segment
from gyguesssong.user.model import User


def _get_authorization_header():
    authorization_header = request.headers.get("Authorization")
    if authorization_header:
        return authorization_header
    authorization_header = request.cookies.get("Authorization")
    if authorization_header:
        return authorization_header
    return None


def _get_current_user():
    authorization_header = _get_authorization_header()
    if not authorization_header:
        return None
    token_raw = _extract_bearer_token(authorization_header)
    token = _decode_bearer_token(token_raw)
    return User(token["id"], token["name"])


def _get_user_ext():
    return current_app.extensions['user_ext']


def _extract_bearer_token(header_raw):
    return header_raw.split()[1]


def _decode_bearer_token(token_raw):
    return user_ext._decode_jwt_token(token_raw)


def _decode_id_token(id_token):
    signing_input, signature_segment = id_token.rsplit(b'.', 1)
    protected_segment, payload_segment = signing_input.split(b'.', 1)
    return json.loads(extract_segment(payload_segment, IDTokenDecodeError).decode())


class UserExt:
    def __init__(self, app=None):
        self._oauth = None
        self._jwt_secret = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        conf_url = app.config.get('USER_EXT_CONF_URL')
        oauth = OAuth(app)
        oauth.register(
            name='user_ext',
            server_metadata_url=conf_url,
            client_kwargs={
                'scope': 'openid profile'
            }
        )

        self._oauth = oauth
        self._jwt_secret = app.config.get('USER_EXT_JWT_SECRET')
        app.extensions["user_ext"] = self

        self._register_blueprint(app)

    @staticmethod
    def _register_blueprint(app):
        from gyguesssong.user.ext.view import bp

        app.register_blueprint(bp)

    def authorize_redirect(self, redirect_uri):
        return self._oauth.user_ext.authorize_redirect(redirect_uri)

    def authorize_jwt_token(self):
        r = self._oauth.user_ext.authorize_access_token()
        payload = _decode_id_token(r['id_token'].encode())
        return self._encode_jwt_token({
            "id": payload['sub'],
            "name": payload["name"]
        })

    @staticmethod
    def set_authorization_response(response, jwt_token):
        response.set_cookie('Authorization', f'Bearer {jwt_token}')

    def _encode_jwt_token(self, raw):
        header = {'alg': 'HS256'}
        return jwt.encode(header, raw, self._jwt_secret).decode()

    def _decode_jwt_token(self, raw):
        return jwt.decode(raw, self._jwt_secret)


class IDTokenDecodeError(Exception):
    pass


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user._get_current_object() is None:
            abort(403)
        return fn(*args, **kwargs)

    return wrapper


current_user = LocalProxy(_get_current_user)
user_ext = LocalProxy(_get_user_ext)
