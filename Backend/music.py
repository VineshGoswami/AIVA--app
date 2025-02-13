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


