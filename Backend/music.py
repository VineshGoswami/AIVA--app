import os
import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = 'your client id key'
SPOTIFY_CLIENT_SECRET = 'your client secret key'
SPOTIFY_REDIRECT_URI = "your redirect url"
SCOPE = "define your scope"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache"
))


def open_spotify():
    subprocess.run(["C:\\Users\\vines\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"])
    time.sleep(5)


def play_song(song_name):
    results = sp.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        devices = sp.devices()
        if devices["devices"]:
            sp.start_playback(uris=[track_uri])
        else:
            print("No active device found. Please open Spotify on your device.")
    else:
        print(f"Song '{song_name}' not found.")


def pause_song():
    sp.pause_playback()


def resume_song():
    sp.start_playback()


def next_song():
    sp.next_track()


def previous_song():
    sp.previous_track()


def create_playlist(name):
    user_id = sp.me()["id"]
    sp.user_playlist_create(user=user_id, name=name, public=True)
    return f"Playlist '{name}' created!"


if __name__ == "__main__":
    print("Spotify authentication complete. Ready to accept commands!")