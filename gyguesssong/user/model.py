from collections import namedtuple
from enum import Enum


class UserStatusInRoom(Enum):
    WAIT_FOR_ROOM_START = 1
    SUGGESTING = 2
    WAIT_FOR_OTHER_SUGGEST = 3
    VOTE_SECTION = 4
    WAIT_FOR_OTHER_VOTE = 5
    WAIT_FOR_NEXT_SECTION = 6
    RESULT = 7


User = namedtuple('User', "id name")
UserStateInRoom = namedtuple('UserStateInRoom', 'status')


def get_user_state_in_room(room):
    # TODO
    pass
