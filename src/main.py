"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from recommender import load_songs, recommend_songs


def run_profile(profile_name: str, user_prefs: dict, songs: list, k: int = 5):
    print(f"\n{'='*50}")
    print(f"Profile: {profile_name}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"  Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs(os.path.join(os.path.dirname(__file__), "../data/songs.csv"))

    profiles = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "target_valence": 0.8,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.2,
            "target_valence": 0.4,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "target_valence": 0.2,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\n{'='*40}")
        print(f"Profile: {profile_name}")
        print(f"{'='*40}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"  Because: {explanation}")
            print()


if __name__ == "__main__":
    main()