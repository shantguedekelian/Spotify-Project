import dash
from dash import html, dcc, Input, Output, State, callback
import pandas as pd
import urllib.parse

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

dash.register_page(__name__, path='/recommend')

df = pd.read_csv("cleaned_spotify_features.csv")  # Contains your clustered song features

layout = html.Div([
    html.H2("🎧 Get Song Recommendations"),
    html.P("Enter a song name you like:"),
    dcc.Input(id="song-input", type="text", placeholder="e.g. Blinding Lights", debounce=True),
    html.Button("Get Recommendations", id="submit-button", n_clicks=0),
    html.Div(id="recommend-output")
])

@callback(
    Output("recommend-output", "children"),
    Input("submit-button", "n_clicks"),
    State("song-input", "value")
)
def recommend_songs(n_clicks, song_input):
    if not song_input:
        return "Please enter a song name."

    # Find close matches (can improve with fuzzy matching or similarity later)
    matches = df[df['track_name'].str.contains(song_input, case=False, na=False)]
    if matches.empty:
        return "No matches found."

    # Get the first match’s cluster and vibe
    cluster = matches.iloc[0]['vibe_cluster']
    genre = matches.iloc[0]['genre']

    # Recommend songs in same cluster (excluding the original)
    recs = df[(df['vibe_cluster'] == cluster) & (~df['track_name'].str.contains(song_input, case=False, na=False)) & (df['genre'] == genre)]
    recs = recs.sort_values('popularity', ascending=False).head(10)
    
    top_songs_table = html.Ul([
    html.Li([
        html.Img(src=get_album_image(row['track_name'], row['artist_name']),
                 style={'height': '64px', 'marginRight': '10px'}),
        html.A(f"{row['track_name']} by {row['artist_name']}",
               href=f"https://open.spotify.com/search/{urllib.parse.quote(row['track_name'] + ' ' + row['artist_name'])}",
               target="_blank")
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'})
    for _, row in recs.iterrows()
])


    return top_songs_table#html.Ul([html.Li(f"{row['track_name']} by {row['artist_name']}") for _, row in recs.iterrows()])