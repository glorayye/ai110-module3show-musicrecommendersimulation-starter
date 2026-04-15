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


def main() -> None:
    songs = load_songs(CSV_PATH)
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.50,
        "target_tempo_bpm": 150,
        "target_danceability": 0.70,
        "target_acousticness": 0.10,
        "likes_acoustic": False,
    }

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