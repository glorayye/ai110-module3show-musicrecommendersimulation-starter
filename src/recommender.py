from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (total_score, reasons)."""
    score = 0.0
    reasons = []

    # --- Categorical matches (binary: match or no match) ---
    if song["genre"] == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if song["mood"] == user_prefs.get("favorite_mood"):
        score += 1.5
        reasons.append(f"mood match: {song['mood']} (+1.5)")

    # --- Numeric closeness scores (1 - |song_value - target|) × weight ---
    energy_score = (1 - abs(song["energy"] - user_prefs.get("target_energy", 0.5))) * 1.0
    score += energy_score
    reasons.append(f"energy closeness: {song['energy']} vs {user_prefs.get('target_energy', 0.5)} (+{energy_score:.2f})")

    valence_score = (1 - abs(song["valence"] - user_prefs.get("target_valence", 0.5))) * 0.75
    score += valence_score
    reasons.append(f"valence closeness: {song['valence']} vs {user_prefs.get('target_valence', 0.5)} (+{valence_score:.2f})")

    tempo_score = (1 - abs(song["tempo_bpm"] / 200 - user_prefs.get("target_tempo_bpm", 120) / 200)) * 0.5
    score += tempo_score
    reasons.append(f"tempo closeness: {song['tempo_bpm']} bpm vs {user_prefs.get('target_tempo_bpm', 120)} (+{tempo_score:.2f})")

    acousticness_score = (1 - abs(song["acousticness"] - user_prefs.get("target_acousticness", 0.5))) * 0.5
    score += acousticness_score
    reasons.append(f"acousticness closeness: {song['acousticness']} vs {user_prefs.get('target_acousticness', 0.5)} (+{acousticness_score:.2f})")

    danceability_score = (1 - abs(song["danceability"] - user_prefs.get("target_danceability", 0.5))) * 0.25
    score += danceability_score
    reasons.append(f"danceability closeness: {song['danceability']} vs {user_prefs.get('target_danceability', 0.5)} (+{danceability_score:.2f})")

    return round(score, 3), reasons


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank by score descending, and return the top k results."""
    scored = [
        (song, score, "\n  ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
