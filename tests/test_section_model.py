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
