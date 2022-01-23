from collections import namedtuple

import spacy

nlp = spacy.load("zh_core_web_sm")

Song = namedtuple('Song', 'uri name artist album')
SongSimilarity = namedtuple('SongSimilarity', 'candidate similarity')


def get_song_similarities(song, candidates):
    similarities = [_get_song_similarity(song, candidate) for candidate in candidates]
    similarities.sort(key=lambda x: x.similarity, reverse=True)
    return similarities


def _get_song_similarity(song, candidate):
    target_tokens = list(_tokenize(song.name))
    candidate_tokens = list(_tokenize(candidate.name))

    all_tokens = set()
    all_tokens.update(target_tokens)
    all_tokens.update(candidate_tokens)

    intersect_tokens = set(target_tokens) & set(candidate_tokens)

    similarity = len(intersect_tokens) / len(all_tokens)
    return SongSimilarity(candidate, similarity)


def _tokenize(text, nlp=nlp):
    for doc in nlp(text):
        yield doc.text
