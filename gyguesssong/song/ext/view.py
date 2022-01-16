from flask import Blueprint, jsonify

from gyguesssong.song.ext import song_search_client
from gyguesssong.song.ext.helper import make_song_json_view
from gyguesssong.user.ext import login_required

bp = Blueprint('song', __name__)


@bp.route("/song/search/<term>/<page:int>")
@login_required
def search_songs(term, page=0):
    songs = song_search_client.search(term, page)
    return jsonify({
        'songs': [make_song_json_view(song) for song in songs]
    })
