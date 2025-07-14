import pandas as pd
import urllib.parse
#Spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="2a79fa55b0a042868c99042ec4277f0d",
    client_secret="326c1de66a1e4c248c97da218414aa71"
))

def get_album_image(track_name, artist_name):
    results = sp.search(q=f"{track_name} {artist_name}", limit=1, type='track')
    if results['tracks']['items']:
        return results['tracks']['items'][0]['album']['images'][0]['url']  # high-res image
    return None

df = pd.read_csv('cleaned_spotify_features3.csv')
# df['link'] = df['index'].apply(lambda x: f"https://open.spotify.com/search/{urllib.parse.quote(df.iloc[x]['track_name']+" "+df.iloc[x]['artist_name'])}")
# df['emoji_vibe'] = df['vibe_cluster'].map({
#     'Hype/Workout': "💪",
#     'Chill & Acoustic': "🌿",
#     'Angry/Intensity': "🔥",
#     'Sad & Soft': "😢",
#     'Feel Good/Dance': "💃",
#     'Moody Intensity': "🌌"
# })

# df['image'] = df.apply(lambda row: get_album_image(row['track_name'], row['artist_name']), axis=1)

# df.head(3)