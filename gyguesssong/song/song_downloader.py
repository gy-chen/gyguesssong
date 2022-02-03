import subprocess
from pathlib import Path

DEFAULT_SONG_DOWNLOAD_EXECUTABLE = Path(__file__).parent / "gyrespot_to_file"


def download_song(track_uri, path, env=None, executable=DEFAULT_SONG_DOWNLOAD_EXECUTABLE):
    subprocess.run([executable, track_uri, path], check=True, env=env)
