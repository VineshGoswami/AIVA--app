import os
import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"

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


def get_active_device(sp):
    devices = sp.devices()["devices"]
    if devices:
        return devices[0]["id"]
    return None


def play_song(song_name):
    results = sp.search(q=song_name, limit=1)
    if not results["tracks"]["items"]:
        print("Song not found.")
        return

    track_uri = results["tracks"]["items"][0]["uri"]
    device_id = get_active_device(sp)

    if not device_id:
        print("No active device found. Please open Spotify on a device.")
        return

    sp.start_playback(device_id=device_id, uris=[track_uri])
    print(f"Playing {song_name} on Spotify.")


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