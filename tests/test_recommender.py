from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- song dict fixtures ---

POP_SONG = {
    "id": 1, "title": "Pop Track", "artist": "A",
    "genre": "pop", "mood": "happy",
    "energy": 0.80, "tempo_bpm": 120, "valence": 0.90,
    "danceability": 0.80, "acousticness": 0.20,
}

LOFI_SONG = {
    "id": 2, "title": "Lofi Loop", "artist": "B",
    "genre": "lofi", "mood": "chill",
    "energy": 0.40, "tempo_bpm": 80, "valence": 0.60,
    "danceability": 0.50, "acousticness": 0.90,
}

ROCK_SONG = {
    "id": 3, "title": "Rock Banger", "artist": "C",
    "genre": "rock", "mood": "intense",
    "energy": 0.91, "tempo_bpm": 152, "valence": 0.48,
    "danceability": 0.66, "acousticness": 0.10,
}


# --- score_song tests ---

def test_score_song_genre_match_adds_points():
    prefs = {"favorite_genre": "pop", "favorite_mood": "sad",
             "target_energy": 0.5, "target_valence": 0.5,
             "target_tempo_bpm": 120, "target_danceability": 0.5,
             "target_acousticness": 0.5, "likes_acoustic": False}
    score_with_match, _ = score_song(prefs, POP_SONG)

    prefs_no_match = {**prefs, "favorite_genre": "jazz"}
    score_no_match, _ = score_song(prefs_no_match, POP_SONG)

    assert score_with_match > score_no_match


def test_score_song_mood_match_adds_points():
    prefs = {"favorite_genre": "jazz", "favorite_mood": "happy",
             "target_energy": 0.5, "target_valence": 0.5,
             "target_tempo_bpm": 120, "target_danceability": 0.5,
             "target_acousticness": 0.5, "likes_acoustic": False}
    score_with_match, _ = score_song(prefs, POP_SONG)

    prefs_no_match = {**prefs, "favorite_mood": "sad"}
    score_no_match, _ = score_song(prefs_no_match, POP_SONG)

    assert score_with_match > score_no_match


def test_score_song_returns_float_and_reasons():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.8, "target_valence": 0.9,
             "target_tempo_bpm": 120, "target_danceability": 0.8,
             "target_acousticness": 0.2, "likes_acoustic": False}
    score, reasons = score_song(prefs, POP_SONG)

    assert isinstance(score, float)
    assert isinstance(reasons, list)
    assert len(reasons) > 0


def test_score_song_perfect_match_near_max():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.80, "target_valence": 0.90,
             "target_tempo_bpm": 120, "target_danceability": 0.80,
             "target_acousticness": 0.20, "likes_acoustic": False}
    score, _ = score_song(prefs, POP_SONG)

    assert score > 6.0  # near-perfect match should be close to max 6.50


def test_score_song_acoustic_penalty_fires():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.8, "target_valence": 0.5,
             "target_tempo_bpm": 120, "target_danceability": 0.5,
             "target_acousticness": 0.5, "likes_acoustic": True}

    # penalty should fire for non-acoustic song (acousticness 0.20 < 0.3)
    score_with_penalty, reasons = score_song(prefs, POP_SONG)
    assert any("penalty" in r for r in reasons)

    # penalty should NOT fire for acoustic song (acousticness 0.90)
    _, reasons_ac = score_song(prefs, LOFI_SONG)
    assert not any("penalty" in r for r in reasons_ac)

    # same song without likes_acoustic should score 1.0 higher (no penalty)
    prefs_no_acoustic = {**prefs, "likes_acoustic": False}
    score_without_penalty, _ = score_song(prefs_no_acoustic, POP_SONG)
    assert round(score_without_penalty - score_with_penalty, 3) == 1.0


# --- recommend_songs tests ---

def test_recommend_songs_returns_top_k():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.8, "target_valence": 0.9,
             "target_tempo_bpm": 120, "target_danceability": 0.8,
             "target_acousticness": 0.2, "likes_acoustic": False}
    results = recommend_songs(prefs, [POP_SONG, LOFI_SONG, ROCK_SONG], k=2)

    assert len(results) == 2


def test_recommend_songs_sorted_descending():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.8, "target_valence": 0.9,
             "target_tempo_bpm": 120, "target_danceability": 0.8,
             "target_acousticness": 0.2, "likes_acoustic": False}
    results = recommend_songs(prefs, [POP_SONG, LOFI_SONG, ROCK_SONG], k=3)
    scores = [score for _, score, _ in results]

    assert scores == sorted(scores, reverse=True)


def test_recommend_songs_pop_profile_ranks_pop_first():
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.8, "target_valence": 0.9,
             "target_tempo_bpm": 120, "target_danceability": 0.8,
             "target_acousticness": 0.2, "likes_acoustic": False}
    results = recommend_songs(prefs, [POP_SONG, LOFI_SONG, ROCK_SONG], k=3)

    assert results[0][0]["genre"] == "pop"


def test_recommend_songs_ghost_profile_returns_results():
    # Genre/mood don't exist — system should still return k results via numeric scoring
    prefs = {"favorite_genre": "bluegrass", "favorite_mood": "nostalgic",
             "target_energy": 0.6, "target_valence": 0.65,
             "target_tempo_bpm": 110, "target_danceability": 0.65,
             "target_acousticness": 0.70, "likes_acoustic": True}
    results = recommend_songs(prefs, [POP_SONG, LOFI_SONG, ROCK_SONG], k=3)

    assert len(results) == 3
    assert all(score >= 0 for _, score, _ in results)
