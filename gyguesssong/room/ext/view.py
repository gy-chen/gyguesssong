from flask import Blueprint, jsonify, abort

from gyguesssong.room import model as room_model
from gyguesssong.room.ext import helper
from gyguesssong.song.ext import song_search_client
from gyguesssong.user.ext import current_user, login_required

bp = Blueprint('room', __name__)


@bp.route("/room/list")
def list_rooms():
    rooms = room_model.list_rooms()
    return jsonify({
        'rooms': [helper.make_room_json_view(room) for room in rooms if
                  room_model.is_room_status_equal(room, model.RoomStatus.WAITING)]
    })


@bp.route('/room/join/<room_id>', methods=['POST'])
@login_required
def join_room(room_id):
    # TODO: add lock
    room = room_model.get_room(room_id)
    if not room:
        abort(400)
    room_model.join_room(room_id, current_user)
    return jsonify({})


@bp.route('/room/joined')
@login_required
def get_joined_room():
    rooms = room_model.list_rooms()
    joined_rooms = [helper.make_room_json_view(room) for room in rooms if
                    room_model.is_user_joined(room, current_user) and not room_model.is_room_status_equal(
                        room_model.RoomStatus.FINISHED)]
    return jsonify({
        'room': joined_rooms[0] if joined_rooms else None
    })


@bp.route('/room/start/<room_id>')
@login_required
def start_room(room_id):
    # TODO: add lock
    room = room_model.get_room(room_id)
    if not room:
        abort(400)
    updated_room = room_model.start_room(room, current_user)
    room_model.set_room(updated_room)
    return jsonify({})


@bp.route("/room/get/<room_id>")
@login_required
def get_room(room_id):
    room = room_model.get_room(room_id)
    if not room:
        abort(400)
    return jsonify({
        'room': helper.make_room_json_view(room)
    })


@bp.route("/room/advance/<room_id>", methods=['POST'])
@login_required
def advance_room(room_id):
    # TODO: add lock
    room = room_model.get_room(room_id)
    if not room:
        abort(400)
    if room_model.can_advance_room_status(room, current_user):
        updated_room = room_model.advance_room_status(room, current_user)
        room_model.set_room(updated_room)
    return jsonify({})


@bp.route('/room/add_candidate_song', methods=['POST'])
@login_required
def add_candidate_song(room_id, uri):
    # TODO: add lock
    room = room_model.get_room(room_id)
    if not room:
        abort(400)
    song = song_search_client.get_song(uri)
    if not song:
        abort(400)
    updated_room = room_model.add_candidate_song(room, song)
    room_model.set_room(updated_room)
    return jsonify({})
