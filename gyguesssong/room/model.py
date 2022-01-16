from collections import namedtuple
from enum import Enum


class RoomStatus(Enum):
    WAITING = 1
    SUGGESTING = 2
    VOTING = 3
    FINISHED = 4


Room = namedtuple('Room', 'id users candidate_songs sections status')


def get_room(id_):
    # TODO
    pass


def set_room(room):
    # TODO
    pass


def list_rooms():
    # TODO
    pass


def create_room(user):
    # TODO
    pass


def get_room_admin_user(room):
    # TODO
    pass


def join_room(room, user):
    # TODO
    pass


def is_user_joined(room, user):
    # TODO
    pass


def is_room_status_equal(room, room_status):
    # TODO
    pass


def start_room(room, user):
    # TODO
    pass


def finish_room(room):
    # TODO
    pass


def can_advance_room_status(room, user):
    # TODO
    pass


def advance_room_status(room, user):
    # TODO
    pass


def add_candidate_song(room, song):
    # TODO
    pass


def can_add_more_candidate_song(room, user):
    # TODO
    pass
