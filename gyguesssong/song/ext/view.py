from flask import Blueprint, jsonify

from gyguesssong.room import model as room_model
from gyguesssong.section import model as section_model
from gyguesssong.song.ext import song_search_client, song_ext
from gyguesssong.song.ext.helper import make_song_json_view
from gyguesssong.user.ext import login_required

bp = Blueprint('song', __name__)


@bp.route("/song/search/<term>/<int:page>")
@login_required
def search_songs(term, page=0):
    songs = song_search_client.search(term, page)
    return jsonify({
        'songs': [make_song_json_view(song) for song in songs]
    })


@bp.route("/song/download/<room_id>/<section_id>")
def download_song(room_id, section_id):
    room = room_model.get_room(room_id)
    section = section_model.get_section(room.sections, section_id)
    return song_ext.serve_downloaded_song(section.correct_song.uri)


@bp.route("/song/_download/<uri>")
def download_song_test(uri):
    song_ext.download_song(uri)
    return '', 204


@bp.route("/song/_serve/<uri>")
def serve_song_test(uri):
    return song_ext.serve_downloaded_song(uri)
