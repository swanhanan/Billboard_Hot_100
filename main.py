from bs4 import BeautifulSoup
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth



response_url ="https://example.com/?code=AQDebAu5lauQ4pLA__3fh508B7QLwDKc09_UdnOysNvh2aRKgScA2izuBcqguWFQYi1bGB_Dw-VkcSYspTT7OxUODSSKlV82a1Pz_4cjRJM1gwSyJmEE2vRzj7q59drpVCIFH_VebhXDI864qvi_j1PtyKD3kQ"
URL= "https://www.billboard.com/charts/hot-100"
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
URI = "http://example.com"

CLIENT_ID = os.environ.get('CL_ID')
CLIENT_SECRET = os.environ.get('CL_SECRET')


USERNAME = os.environ.get('SPOTIFY_CL_ID')
ACCESS_TOKEN = os.environ.get('SPOTIFY_ACCESS_TOKEN')

travel_year = input("Which year do you want to travl to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel_year}/")
html_page = response.text
soup = BeautifulSoup(html_page, "html.parser")

heading_titles = soup.find_all(name="h3")
songs = [song.getText().strip() for song in heading_titles]
song_titles = songs[3:103]

print(song_titles)

sp = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=URI,  username=USERNAME, scope="playlist-modify-private", cache_path="token.txt")
token = sp.get_access_token()


credentials = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
credentials_token = credentials.get_access_token()
user = spotipy.client.Spotify(auth=ACCESS_TOKEN, requests_session=True, client_credentials_manager=credentials, oauth_manager=sp, auth_manager=sp, proxies=None, requests_timeout=5, status_forcelist=None, retries=3, status_retries=3, backoff_factor=0.3, language=None)

year = travel_year.split("-")[0]
song_uris = []
for song in song_titles:
    result = user.search(f"track: {song} year: {year}", type='track')
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

user_id = user.me()['id']
new_playlist = user.user_playlist_create(user_id, f"{year} Billboard 100", public=False)
PLAYLIST_ID = new_playlist["id"]
user.playlist_add_items(playlist_id=PLAYLIST_ID, items=song_titles, position=None)