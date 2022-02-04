from collections import namedtuple
from enum import Enum
from uuid import uuid4


class IllegalSectionStatusError(Exception):
    pass


class AlreadyVotedError(Exception):
    pass


class SectionStatus(Enum):
    PREPARING = 1
    VOTING = 2
    WAIT_FINISH = 3
    FINISHED = 4


Section = namedtuple('Section', 'section_id status correct_song candidate_songs votes scores')
Vote = namedtuple('Vote', 'vote_song_uri user')
Score = namedtuple('Score', 'point user')


def generate_section_id():
    return str(uuid4())


def create_section(section_id, correct_song, candidate_songs):
    return Section(
        section_id,
        SectionStatus.PREPARING,
        correct_song,
        candidate_songs,
        (),
        ()
    )


def get_section(sections, section_id):
    for section in sections:
        if section.section_id == section_id:
            return section
    return None


def is_voted(section, user):
    for vote in section.votes:
        if vote.user.id == user.id:
            return True
    return False


def vote(section, vote_song_uri, user):
    if not section_status_is(section, SectionStatus.VOTING):
        raise IllegalSectionStatusError()
    if is_voted(section, user):
        raise AlreadyVotedError()
    return _vote(section, vote_song_uri, user)


def _vote(section, vote_song_uri, user):
    return _copy_section(section, votes=tuple(Vote(vote_song_uri, user), *section.votes))


def section_status_is(section, status):
    return section.status == status


class SectionAdvanceDirection(Enum):
    PREPARING_TO_VOTING = 1
    VOTING_TO_WAIT_FINISH = 2
    WAIT_FINISH_TO_FINISHED = 3


def can_advance_section_status(section, all_users, is_owner):
    if section_status_is(section, SectionStatus.PREPARING):
        return SectionAdvanceDirection.PREPARING_TO_VOTING
    elif section_status_is(section, SectionStatus.VOTING):
        voted_users = set(vote.user for vote in section.votes)
        all_users = set(all_users)
        is_all_users_voted = len(all_users - voted_users) == 0
        return SectionAdvanceDirection.VOTING_TO_WAIT_FINISH if is_all_users_voted else None
    elif section_status_is(section, SectionStatus.WAIT_FINISH):
        return SectionAdvanceDirection.WAIT_FINISH_TO_FINISHED if is_owner else None
    elif section_status_is(section, SectionStatus.FINISHED):
        return None
    return None


def advance_section_status(section, direction, scores=None):
    if direction == SectionAdvanceDirection.PREPARING_TO_VOTING:
        return _copy_section(section, status=SectionStatus.VOTING)
    elif direction == SectionAdvanceDirection.VOTING_TO_WAIT_FINISH:
        return _copy_section(section, status=SectionStatus.WAIT_FINISH, scores=scores)
    elif direction == SectionAdvanceDirection.WAIT_FINISH_TO_FINISHED:
        return _copy_section(section, status=SectionStatus.FINISHED)
    assert False


CORRECT_SCORE_LEVELS = (4, 2, 1, 0, -1, -2)
INCORRECT_SCORE_LEVELS = (-4, -2, -1, -2, -4)


def _create_scores_pool(data_len, score_levels, padding_score_index):
    return score_levels[:padding_score_index] + \
           score_levels[padding_score_index:padding_score_index + 1] * min(data_len - len(score_levels), 0) + \
           score_levels[padding_score_index + 1:]


def calculate_scores(correct_song, votes):
    """Calculate scores from the votes

    :param correct_song:
    :param votes:
    :return: scores:
    """
    corrects = tuple(vote for vote in votes if vote.vote_song_uri == correct_song.uri)
    incorrects = tuple(vote for vote in votes if vote.vote_song_uri != correct_song.uri)
    correct_scores_pool = _create_scores_pool(len(corrects), CORRECT_SCORE_LEVELS, 3)
    incorrect_scores_pool = _create_scores_pool(len(incorrects), INCORRECT_SCORE_LEVELS, 2)
    result = []
    for correct in corrects:
        result.append(Score(correct_scores_pool.pop(0), correct.user))
    for incorrect in incorrects:
        result.append(Score(incorrect_scores_pool.pop(0), incorrect.user))
    result.sort(key=lambda s: s.point, reverse=True)
    return tuple(result)


def _copy_section(section, status=None, correct_song=None, candidate_songs=None, votes=None, scores=None):
    return Section(
        section.id,
        section.status if status is None else status,
        section.corrent_song if correct_song is None else correct_song,
        section.candidate_songs if candidate_songs is None else candidate_songs,
        tuple(vote, *section.votes) if votes is None else votes,
        section.scores if scores is None else scores
    )
