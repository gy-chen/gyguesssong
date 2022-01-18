from collections import namedtuple
from enum import Enum


class SectionStatus(Enum):
    PREPARING = 1
    VOTING = 2
    WAIT_FINISH = 3
    FINISHED = 4


Section = namedtuple('Section', 'status correct_song correct_song_download_url candidate_songs votes scores')
Vote = namedtuple('Vote', 'vote_song_uri user')
Score = namedtuple('Score', 'point user')


def create_section(correct_song, candidate_songs):
    # TODO:
    pass


def is_voted(section, user):
    # TODO
    pass


def vote(section, vote_song_uri, user):
    # TODO
    pass


def can_advance_section_status(section, user, all_users):
    # TODO
    pass


def advance_section_status(section, user, all_users):
    # TODO
    pass


def calculate_scores(votes):
    # TODO
    pass
