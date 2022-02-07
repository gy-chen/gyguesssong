import pytest

from gyguesssong.section import model
from gyguesssong.song.model import Song
from gyguesssong.user.model import User


@pytest.fixture
def sample_correct_song():
    return Song(uri='spotify:track:4TJlU2Vg1e0FDOdQhqF246', name='安靜', artist='Jay Chou', album='范特西')


@pytest.fixture
def sample_candidate_songs():
    return (
        Song(uri='spotify:track:17qKg76rSQRL6ilaEKGYQX', name='安靜了', artist='S.H.E', album='我的電台 FM S.H.E'),
        Song(uri='spotify:track:5GUdAU8jH5l9qMzztZxhwX', name='安靜的美好', artist='康士坦的變化球', album='更迭'),
        Song(uri='spotify:track:2rqkp8IoJ6PtlXu6VrnPR1', name='白噪音 ASMR空靈頌缽: 安靜的心靈', artist='Noble Music Project',
             album='白噪音 冥想 頌缽 森林ASMR氛圍之聲')
    )


def test_generate_section_id():
    assert model.generate_section_id()
    assert isinstance(model.generate_section_id(), str)


def test_create_section(sample_correct_song, sample_candidate_songs):
    sample_section_id = model.generate_section_id()
    section = model.create_section(
        sample_section_id,
        sample_correct_song,
        sample_candidate_songs
    )
    assert isinstance(section, model.Section)
    assert section.section_id == sample_section_id
    assert section.correct_song == sample_correct_song
    assert section.candidate_songs == sample_candidate_songs
    assert section.status == model.SectionStatus.PREPARING
    assert section.votes == ()
    assert section.scores == ()


def test_get_section(sample_correct_song, sample_candidate_songs):
    section_id_1 = model.generate_section_id()
    section_id_2 = model.generate_section_id()
    section_id_3 = model.generate_section_id()

    section_1 = model.create_section(
        section_id_1,
        sample_correct_song,
        sample_candidate_songs
    )
    section_2 = model.create_section(
        section_id_2,
        sample_correct_song,
        sample_candidate_songs
    )
    section_3 = model.create_section(
        section_id_3,
        sample_correct_song,
        sample_candidate_songs
    )

    sections = (section_2, section_3, section_1)

    assert model.get_section(sections, section_id_1) == section_1
    assert model.get_section(sections, section_id_2) == section_2
    assert model.get_section(sections, section_id_3) == section_3


def test_is_voted(sample_correct_song, sample_candidate_songs):
    section_id = model.generate_section_id()
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')

    section = model.Section(
        section_id,
        model.SectionStatus.VOTING,
        sample_correct_song,
        sample_candidate_songs,
        (model.Vote('spotify:track:1CwyAyTN9nohNMWsJWFGY2', user1),),
        ()
    )

    assert model.is_voted(section, user1)
    assert not model.is_voted(section, user2)


def test_vote(sample_correct_song, sample_candidate_songs):
    section_id = model.generate_section_id()
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')

    section = model.Section(
        section_id,
        model.SectionStatus.VOTING,
        sample_correct_song,
        sample_candidate_songs,
        (),
        ()
    )

    voted_section = model.vote(section, 'spotify:track:1CwyAyTN9nohNMWsJWFGY2', user1)
    assert model.is_voted(voted_section, user1)
    assert not model.is_voted(voted_section, user2)
    assert model.Vote('spotify:track:1CwyAyTN9nohNMWsJWFGY2', user1) in voted_section.votes

    voted_section = model.vote(voted_section, sample_correct_song.uri, user2)
    assert model.is_voted(voted_section, user1)
    assert model.is_voted(voted_section, user2)
    assert model.Vote('spotify:track:1CwyAyTN9nohNMWsJWFGY2', user1) in voted_section.votes
    assert model.Vote(sample_correct_song.uri, user2) in voted_section.votes


def test_can_advance_to_voting(sample_correct_song, sample_candidate_songs):
    section_id = model.generate_section_id()
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')
    users = (user1, user2)

    section = model.Section(
        section_id,
        model.SectionStatus.PREPARING,
        sample_correct_song,
        sample_candidate_songs,
        (),
        ()
    )

    assert model.can_advance_section_status(section, users, False) == model.SectionAdvanceDirection.PREPARING_TO_VOTING


def test_can_advance_to_wait_finish(sample_correct_song, sample_candidate_songs):
    section_id = model.generate_section_id()
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')
    users = (user1, user2)

    vote1 = model.Vote('spotify:track:1CwyAyTN9nohNMWsJWFGY2', user1)

    section_not_all_voted = model.Section(
        section_id,
        model.SectionStatus.VOTING,
        sample_correct_song,
        sample_candidate_songs,
        (vote1,),
        ()
    )
    assert model.can_advance_section_status(section_not_all_voted, users, False) is None

    vote2 = model.Vote(sample_correct_song.uri, user2)
    votes = (vote1, vote2)
    section_all_voted = model.Section(
        section_id,
        model.SectionStatus.VOTING,
        sample_correct_song,
        sample_candidate_songs,
        votes,
        ()
    )
    assert model.can_advance_section_status(section_all_voted, users,
                                            False) == model.SectionAdvanceDirection.VOTING_TO_WAIT_FINISH


def test_can_advance_to_finish(sample_correct_song, sample_candidate_songs):
    section_id = model.generate_section_id()
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')
    users = (user1, user2)

    section = model.Section(
        section_id,
        model.SectionStatus.WAIT_FINISH,
        sample_correct_song,
        sample_candidate_songs,
        (),
        ()
    )

    assert model.can_advance_section_status(section, users, False) is None
    assert model.can_advance_section_status(section, users,
                                            True) == model.SectionAdvanceDirection.WAIT_FINISH_TO_FINISHED


def test_calculate_scores_small_size(sample_correct_song):
    # correct votes
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')
    user3 = User('id3', 'name3')
    vote1 = model.Vote(sample_correct_song.uri, user1)  # 4
    vote2 = model.Vote(sample_correct_song.uri, user2)  # 2
    vote3 = model.Vote(sample_correct_song.uri, user3)  # 1
    # incorrect votes
    user4 = User('id4', 'name4')
    user5 = User('id5', 'name5')
    user6 = User('id6', 'name6')
    vote4 = model.Vote('spotify:track:17qKg76rSQRL6ilaEKGYQX', user4)  # -4
    vote5 = model.Vote('spotify:track:5GUdAU8jH5l9qMzztZxhwX', user5)  # -2
    vote6 = model.Vote('spotify:track:2rqkp8IoJ6PtlXu6VrnPR1', user6)  # -1

    votes = (vote1, vote2, vote3, vote4, vote5, vote6)
    scores = model.calculate_scores(sample_correct_song, votes)
    assert len(scores) == 6
    assert scores[0].point == 4
    assert scores[0].user == user1
    assert scores[1].point == 2
    assert scores[1].user == user2
    assert scores[2].point == 1
    assert scores[2].user == user3
    assert scores[3].point == -1
    assert scores[3].user == user6
    assert scores[4].point == -2
    assert scores[4].user == user5
    assert scores[5].point == -4
    assert scores[5].user == user4


def test_calculate_scores_large_size(sample_correct_song):
    # correct votes
    user1 = User('id1', 'name1')
    user2 = User('id2', 'name2')
    user3 = User('id3', 'name3')
    user4 = User('id4', 'name4')
    user5 = User('id5', 'name5')
    user6 = User('id6', 'name6')
    user7 = User('id7', 'name7')
    user8 = User('id8', 'name8')
    vote1 = model.Vote(sample_correct_song.uri, user1)  # 4
    vote2 = model.Vote(sample_correct_song.uri, user2)  # 2
    vote3 = model.Vote(sample_correct_song.uri, user3)  # 1
    vote4 = model.Vote(sample_correct_song.uri, user4)  # 0
    vote5 = model.Vote(sample_correct_song.uri, user5)  # 0
    vote6 = model.Vote(sample_correct_song.uri, user6)  # 0
    vote7 = model.Vote(sample_correct_song.uri, user7)  # -1
    vote8 = model.Vote(sample_correct_song.uri, user8)  # -2
    # incorrect votes
    user9 = User('id9', 'name9')
    user10 = User('id10', 'name10')
    user11 = User('id11', 'name11')
    user12 = User('id12', 'name12')
    user13 = User('id13', 'name13')
    user14 = User('id14', 'name14')
    user15 = User('id15', 'name15')
    vote9 = model.Vote('spotify:track:4ZntdEEXpiWVOev9sO5Ap0', user9)  # -4
    vote10 = model.Vote('spotify:track:3OeAylnJlt6aGePGtr4Ozt', user10)  # -2
    vote11 = model.Vote('spotify:track:7HaqRYmhwbzIubHe6v1b9p', user11)  # -1
    vote12 = model.Vote('spotify:track:1uIURU2HSV5HdmfqB2aiVm', user12)  # -1
    vote13 = model.Vote('spotify:track:3Ch1Seg9ODLvU8quPtMJxw', user13)  # -1
    vote14 = model.Vote('spotify:track:0wrnCaBk0ZXu977APtFbQb', user14)  # -2
    vote15 = model.Vote('spotify:track:1Pr5jwcGT9Bii8v4Dn9gGP', user15)  # -4

    votes = (
        vote1, vote2, vote3, vote4, vote5, vote6, vote7, vote8, vote9, vote10, vote11, vote12, vote13, vote14, vote15)

    scores = model.calculate_scores(sample_correct_song, votes)

    assert len(scores) == 15
    assert scores == (model.Score(point=4, user=User(id='id1', name='name1')),
                      model.Score(point=2, user=User(id='id2', name='name2')),
                      model.Score(point=1, user=User(id='id3', name='name3')),
                      model.Score(point=0, user=User(id='id4', name='name4')),
                      model.Score(point=0, user=User(id='id5', name='name5')),
                      model.Score(point=0, user=User(id='id6', name='name6')),
                      model.Score(point=-1, user=User(id='id7', name='name7')),
                      model.Score(point=-1, user=User(id='id11', name='name11')),
                      model.Score(point=-1, user=User(id='id12', name='name12')),
                      model.Score(point=-1, user=User(id='id13', name='name13')),
                      model.Score(point=-2, user=User(id='id8', name='name8')),
                      model.Score(point=-2, user=User(id='id10', name='name10')),
                      model.Score(point=-2, user=User(id='id14', name='name14')),
                      model.Score(point=-4, user=User(id='id9', name='name9')),
                      model.Score(point=-4, user=User(id='id15', name='name15')))
