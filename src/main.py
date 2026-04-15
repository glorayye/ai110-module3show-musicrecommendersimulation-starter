"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


PROFILES = {
    # --- Standard profiles ---

    # High-energy rock listener
    "intense": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.50,
        "target_tempo_bpm": 150,
        "target_danceability": 0.70,
        "target_acousticness": 0.10,
        "likes_acoustic": False,
    },

    # Late-night study listener
    "chill": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "target_valence": 0.58,
        "target_tempo_bpm": 75,
        "target_danceability": 0.60,
        "target_acousticness": 0.80,
        "likes_acoustic": True,
    },

    # Feel-good pop listener
    "upbeat": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.82,
        "target_tempo_bpm": 120,
        "target_danceability": 0.83,
        "target_acousticness": 0.25,
        "likes_acoustic": False,
    },

    # --- Adversarial / edge case profiles ---

    # GHOST: genre and mood that don't exist in the catalog.
    # Expected: system gets 0 pts on both categorical signals for every song —
    # winner is decided entirely by numeric closeness. Reveals whether numeric
    # weights alone produce a sensible ranking or random-feeling results.
    "ghost": {
        "favorite_genre": "bluegrass",
        "favorite_mood": "nostalgic",
        "target_energy": 0.60,
        "target_valence": 0.65,
        "target_tempo_bpm": 110,
        "target_danceability": 0.65,
        "target_acousticness": 0.70,
        "likes_acoustic": True,
    },

    # CONTRADICTION: numeric targets match a chill/acoustic song (Clair de Lune),
    # but genre/mood labels point at metalcore. Tests whether genre dominance
    # (+2.0) overrides what the numbers clearly say.
    "contradiction": {
        "favorite_genre": "metalcore",
        "favorite_mood": "aggressive",
        "target_energy": 0.18,        # matches Clair de Lune exactly
        "target_valence": 0.62,
        "target_tempo_bpm": 58,
        "target_danceability": 0.22,
        "target_acousticness": 0.98,  # strongly acoustic
        "likes_acoustic": True,
    },

    # EXTREMES: every numeric target pushed to maximum.
    # Tests for score inflation — does a song score well just by being
    # "high on everything" even if genre/mood don't match at all?
    "extremes": {
        "favorite_genre": "latin",
        "favorite_mood": "triumphant",
        "target_energy": 1.0,
        "target_valence": 1.0,
        "target_tempo_bpm": 200,
        "target_danceability": 1.0,
        "target_acousticness": 1.0,
        "likes_acoustic": True,
    },
}

# Swap the key below to test a different profile
ACTIVE_PROFILE = "extremes"


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded songs: {len(songs)}")

    user_prefs = PROFILES[ACTIVE_PROFILE]
    print(f"Active profile: {ACTIVE_PROFILE}\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']}  —  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 6.50")
        print("    Why:")
        for line in explanation.split("\n"):
            print(f"      {line.strip()}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()