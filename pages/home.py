import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
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





dash.register_page(__name__, path='/')

# Load your data
df = pd.read_csv("cleaned_spotify_features.csv")

layout = html.Div([
    html.H1("🎵 Song Explorer by Mood"),

    html.Label("Filter by Vibe:"),
    dcc.Dropdown(
        options=[{'label': vibe, 'value': vibe} for vibe in df['vibe_cluster'].unique()],
        value=None,
        id='vibe-filter',
        multi=True
    ),

    #genre search
    html.Label("Search by Genre:"),
    dcc.Input(id='genre-input', type='text', placeholder='e.g. pop, rap'),
    
    #artist search
    html.Label("Search by Artist:"),
    dcc.Input(id='artist-input', type='text', placeholder='e.g. Drake, Taylor Swift'),

    dcc.Graph(id='scatter-plot'),
    
    html.H3("Top 10 Songs by Popularity"),
    html.Div(id='top-songs'),

    html.Div(id='song-details', style={'marginTop': 20})
    
])

@callback(
    Output('scatter-plot', 'figure'),
    Output('top-songs', 'children'),
    Input('vibe-filter', 'value'),
    Input('genre-input', 'value'),
    Input('artist-input', 'value')
)
def update_plot(selected_vibes, genre_text, artist_text):
    filtered_df = df.copy()

    # Filter by vibe
    if selected_vibes:
        filtered_df = filtered_df[filtered_df['vibe_cluster'].isin(selected_vibes)]

    # Filter by genre
    if genre_text:
        filtered_df = filtered_df[filtered_df['genre'].str.contains(genre_text, case=False, na=False)]

    # Filter by artist
    if artist_text:
        #filtered_df = filtered_df[filtered_df['artist_name'].str.contains(artist_text, case=False, na=False)]
        filtered_df = filtered_df[filtered_df['artist_name'].str.lower() == artist_text.lower()]
        
    fig = px.scatter(
        filtered_df, x='PCA1', y='PCA2',
        color='vibe_cluster',
        hover_data=['track_name', 'artist_name', 'genre'],
        title="Songs by Mood/Vibe"
    )
    
    # Get top 10 songs by popularity
    top_songs = filtered_df.sort_values(by='popularity', ascending=False).head(10)

    # Format as HTML table
    top_songs_table = html.Ul([
    html.Li([
        html.Img(src=get_album_image(row['track_name'], row['artist_name']),
                 style={'height': '64px', 'marginRight': '10px'}),
        html.A(f"{row['track_name']} by {row['artist_name']}",
               href=f"https://open.spotify.com/search/{urllib.parse.quote(row['track_name'] + ' ' + row['artist_name'])}",
               target="_blank")
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'})
    for _, row in top_songs.iterrows()
])

    return fig, top_songs_table

# if __name__ == '__main__':
#     app.run(debug=True) 