from flask import Blueprint, jsonify, url_for, redirect

from gyguesssong.room import model as room_model
from gyguesssong.user import model as user_model
from gyguesssong.user.ext import user_ext, helper, login_required, current_user
from gyguesssong.user.ext.helper import user_to_json_view

bp = Blueprint('user', __name__)


@bp.route("/user/room_state")
@login_required
def get_user_state_in_room():
    joined_rooms = [room for room in room_model.list_rooms()
                    if not room_model.is_room_status_equal(room,
                                                           room_model.RoomStatus.FINISHED) and
                    room_model.is_user_joined(room, current_user)]
    if not joined_rooms:
        return jsonify({

        })
    joined_room = joined_rooms[0]
    user_state_in_room = user_model.get_user_state_in_room(joined_room, current_user)
    return jsonify(helper.user_state_in_room_to_json_view(user_state_in_room))


@bp.route("/user/profile")
@login_required
def user_profile():
    return jsonify(user_to_json_view(current_user))


@bp.route("/login")
def login():
    redirect_url = url_for(".login_redirect", _external=True)
    return user_ext.authorize_redirect(redirect_url)


@bp.route("/login/redirect")
def login_redirect():
    jwt_token = user_ext.authorize_jwt_token()
    response = redirect("/")
    user_ext.set_authorization_response(response, jwt_token)
    return response
