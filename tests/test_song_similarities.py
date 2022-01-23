import pytest

from gyguesssong.song.model import Song, get_song_similarities, SongSimilarity


@pytest.fixture
def sample_songs():
    return [Song(uri='spotify:track:4TJlU2Vg1e0FDOdQhqF246', name='安靜', artist='Jay Chou', album='范特西'),
            Song(uri='spotify:track:17qKg76rSQRL6ilaEKGYQX', name='安靜了', artist='S.H.E', album='我的電台 FM S.H.E'),
            Song(uri='spotify:track:5GUdAU8jH5l9qMzztZxhwX', name='安靜的美好', artist='康士坦的變化球', album='更迭'),
            Song(uri='spotify:track:2rqkp8IoJ6PtlXu6VrnPR1', name='白噪音 ASMR空靈頌缽: 安靜的心靈', artist='Noble Music Project',
                 album='白噪音 冥想 頌缽 森林ASMR氛圍之聲'),
            Song(uri='spotify:track:7GVw2UGhVbBpq6fqiSlPUV', name='佇世界安靜的時', artist='Sorry Youth', album='歹勢好勢'),
            Song(uri='spotify:track:3SViwkY1IP8cVvcBmcIkxn', name='一直很安靜', artist='阿桑', album='寂寞在唱歌'),
            Song(uri='spotify:track:1CwyAyTN9nohNMWsJWFGY2', name='20首安靜音樂為了放鬆', artist='睡覺音樂',
                 album='20首安靜音樂為了放鬆: α波催眠曲, 幫助舒緩抑鬱症, 睡覺和治療失眠'),
            Song(uri='spotify:track:2LTrObTrNFwgb1ICMcC6xg', name='安靜 - Instrumental', artist='純音樂',
                 album='2002鋼琴戀曲PIANO HITS'),
            Song(uri='spotify:track:1H3AJl1iMNLLovKO35iE3t', name='安靜', artist='Stream of Praise',
                 album='找一個地方 (安靜演奏專輯2)'),
            Song(uri='spotify:track:6OI0p9YgcC82jIciqUjcta', name='我是不是該安靜的走開', artist='Aaron Kwok',
                 album='我是不是該安靜的走開'),
            Song(uri='spotify:track:796dHtvKjm1IvBnWG2NomS', name='當世界安靜 - Unplugged Originals', artist='Rose Liu',
                 album='Unplugged Originals - Part 3'),
            Song(uri='spotify:track:11QR4qgYtLvV9t0o1yDOFn', name='安靜', artist='Joshua Band', album='直到世界盡頭'),
            Song(uri='spotify:track:0yjL2wlKaIZaDKaGdrVwEn', name='安靜的午後', artist='Pianoboy高至豪', album='Pianoboy'),
            Song(uri='spotify:track:1Pr5jwcGT9Bii8v4Dn9gGP', name='怕安靜', artist='Show Luo', album='獨一無二'),
            Song(uri='spotify:track:0wrnCaBk0ZXu977APtFbQb', name='我只想欲安靜', artist='草屯囝仔', album='貓霧仔光'),
            Song(uri='spotify:track:3Ch1Seg9ODLvU8quPtMJxw', name='一直很安靜', artist='趙登凱', album='一直很安靜(青春重置計畫 3 劇好聽)'),
            Song(uri='spotify:track:1uIURU2HSV5HdmfqB2aiVm', name='安靜了太久 (電影《藍波:最後一滴血》中文宣傳曲)', artist='K.R Bros',
                 album='安靜了太久 (電影《藍波:最後一滴血》中文宣傳曲)'),
            Song(uri='spotify:track:7HaqRYmhwbzIubHe6v1b9p', name='安靜', artist='Stream of Praise',
                 album='能不能 (鋼琴演奏專輯3)'),
            Song(uri='spotify:track:3OeAylnJlt6aGePGtr4Ozt', name='安靜 - 三立、台視偶像劇《愛上哥們》插曲', artist='Miu Chu, Andrew Tan',
                 album='My Way'),
            Song(uri='spotify:track:4ZntdEEXpiWVOev9sO5Ap0', name='安靜', artist='Jay Chou', album='The One 演唱會')]


def test_song_similarities(sample_songs):
    target_song = sample_songs[0]
    for song_similarity in get_song_similarities(target_song, sample_songs):
        assert isinstance(song_similarity, SongSimilarity)
        assert isinstance(song_similarity.candidate, Song)
