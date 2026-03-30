from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import math

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
        # Score each song and return top-k songs sorted by score (descending)
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = score_song(user, song)
            scored.append((song, score))

        scored.sort(key=lambda t: t[1], reverse=True)
        return [t[0] for t in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, explanation = score_song(user, song)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields converted."""
    songs: List[Dict] = []
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # convert numeric fields
            try:
                row_parsed = {
                    "id": int(row["id"]),
                    "title": row.get("title", ""),
                    "artist": row.get("artist", ""),
                    "genre": row.get("genre", ""),
                    "mood": row.get("mood", ""),
                    "energy": float(row.get("energy", 0.0)),
                    "tempo_bpm": float(row.get("tempo_bpm", 0.0)),
                    "valence": float(row.get("valence", 0.0)),
                    "danceability": float(row.get("danceability", 0.0)),
                    "acousticness": float(row.get("acousticness", 0.0)),
                }
            except Exception:
                # If parsing fails for a row, skip it
                continue
            songs.append(row_parsed)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user_prefs and return the top-k as (song, score, explanation) tuples."""
    # Convert dict-based prefs to scoring directly
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, explanation = score_song_from_prefs(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[:k]


def _clamp01(x: float) -> float:
    """Clamp a float to the range [0.0, 1.0]."""
    return max(0.0, min(1.0, float(x)))


def score_song(user: UserProfile, song: Song) -> Tuple[float, str]:
    """Score a Song for a UserProfile. Returns (score, explanation).

    Scoring rules (per request):
    +2.0 if song.genre == user.favorite_genre
    +1.0 if song.mood == user.favorite_mood
    +1.0 * (1.0 - abs(song.energy - user.target_energy))
    +1.0 * (1.0 - abs(song.valence - user.target_valence))
    """
    # Weights
    genre_w = 2.0
    mood_w = 1.0
    energy_w = 1.0
    valence_w = 1.0

    parts: List[str] = []
    total = 0.0

    if song.genre == user.favorite_genre:
        total += genre_w
        parts.append(f"genre match (+{genre_w:.1f})")

    if song.mood == user.favorite_mood:
        total += mood_w
        parts.append(f"mood match (+{mood_w:.1f})")

    e_score = energy_w * (1.0 - abs(_clamp01(song.energy) - _clamp01(user.target_energy)))
    total += e_score
    parts.append(f"energy closeness (+{e_score:.2f})")

    v_score = valence_w * (1.0 - abs(_clamp01(song.valence) - _clamp01(user.target_valence)))
    total += v_score
    parts.append(f"valence closeness (+{v_score:.2f})")

    explanation = "; ".join(parts)
    return total, explanation


def score_song_from_prefs(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
   """Score a dict-based song against dict-based user prefs. Returns (score, explanation)."""
    # Mirror the same scoring logic as score_song
    genre_w = 2.0
    mood_w = 1.0
    energy_w = 1.0
    valence_w = 1.0

    parts: List[str] = []
    total = 0.0

    song_genre = song.get("genre", "")
    song_mood = song.get("mood", "")
    song_energy = float(song.get("energy", 0.0))
    song_valence = float(song.get("valence", 0.0))

    if song_genre == user_prefs.get("favorite_genre"):
        total += genre_w
        parts.append(f"genre match (+{genre_w:.1f})")

    if song_mood == user_prefs.get("favorite_mood"):
        total += mood_w
        parts.append(f"mood match (+{mood_w:.1f})")

    e_score = energy_w * (1.0 - abs(_clamp01(song_energy) - _clamp01(user_prefs.get("target_energy", 0.0))))
    total += e_score
    parts.append(f"energy closeness (+{e_score:.2f})")

    v_score = valence_w * (1.0 - abs(_clamp01(song_valence) - _clamp01(user_prefs.get("target_valence", 0.0))))
    total += v_score
    parts.append(f"valence closeness (+{v_score:.2f})")

    explanation = "; ".join(parts)
    return total, explanation
