from flask import Blueprint, jsonify

from gyguesssong.room import model as room_model
from gyguesssong.user import model as user_model
from gyguesssong.user.ext import helper
from gyguesssong.user.ext import login_required, current_user

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
