import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import urllib.parse

dash.register_page(__name__, path='/')

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





# Load your data
df = pd.read_csv("cleaned_spotify_features.csv")
df = df.drop(columns=['index'], axis=1).reset_index()
df['link'] = df['index'].apply(lambda x: f"https://open.spotify.com/search/{urllib.parse.quote(df.iloc[x]['track_name']+" "+df.iloc[x]['artist_name'])}")
df['emoji_vibe'] = df['vibe_cluster'].map({
    'Hype/Workout': "💪",
    'Chill & Acoustic': "🌿",
    'Angry/Intensity': "🔥",
    'Sad & Soft': "😢",
    'Feel Good/Dance': "💃",
    'Moody Intensity': "🌌"
})

customdata = df[["track_name", "artist_name", "genre", "emoji_vibe", "vibe_cluster", "link"]].values


layout = html.Div([
    html.H1("🎵 Song Explorer by Mood"),

    html.Label("Filter by Vibe:"),
    
    html.Div([
    dcc.Dropdown(
        options=[{'label': vibe, 'value': vibe} for vibe in df['vibe_cluster'].unique()],
        value=None,
        id='vibe-filter',
        multi=True,
        dropdownStyle={
        'backgroundColor': '#2c2c2c', # dropdown options bg
        'color': '#f0f0f0',             # dropdown options text
        }
    ),
    ], className="input-container"),

    #genre search
    html.Label("Search by Genre:"),
    dcc.Input(id='genre-input', type='text', placeholder='e.g. pop, rap'),
    
    #artist search
    html.Label("Search by Artist:"),
    dcc.Input(id='artist-input', type='text', placeholder='e.g. Drake, Taylor Swift'),


    html.Div([
        dcc.Graph(id='scatter-plot', clickData=None),
        html.Div(id='song-info', className="song-info-box")
    ], className="graph-container"),
    
    html.H3("Top 10 Songs by Popularity"),
    
    html.Div(id='top-songs', className="top-songs-box"),

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
        
    customdata2 = filtered_df[["track_name", "artist_name", "genre", "emoji_vibe", "vibe_cluster", "link"]].values

    fig = px.scatter(
        filtered_df, x='PCA1', y='PCA2',
        color='vibe_cluster',
        hover_data=['track_name', 'artist_name', 'genre'],
        title="Songs by Mood/Vibe",
        #custom_data=customdata2
    )
    
    fig.update_layout(
        title={
        'text': "Songs by Vibe",
        'y': 0.97,  # vertical position
        'x': 0.5,   # horizontal centering
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'size': 28,  # make it bigger
            }
        },
        
        xaxis=dict(showticklabels=False, title=None),
        yaxis=dict(showticklabels=False, title=None),
        plot_bgcolor="#48494B",     # Plot background
        paper_bgcolor="#48494B",    # Outer background
        font_color="#D9DDDC",
        margin=dict(l=20, r=20, t=40, b=20),
        
        legend=dict(
        title='Vibe',  # Rename legend title
        font=dict(
            size=16,     # Bigger text
            family="Roboto, sans-serif",
            color="white"
        ),
        title_font=dict(
            size=18,
            family="Roboto, sans-serif",
            color="white"
        ),
        itemsizing='constant',  # Keep consistent size
        )
    )

    fig.update_traces(
        hovertemplate=
            "<b>%{customdata[0]}</b> %{customdata[3]}<br>" +  # track_name + emoji
            "Artist: %{customdata[1]}<br>" +                  # artist_name
            "Vibe: %{customdata[4]}<br>" +                    # vibe_cluster name
            "Genre: %{customdata[2]}<br>" +                   # genre
            #"<a href='%{customdata[6]}' target='_blank'>🎧 Listen</a>" +  # spotify_url
            "<extra></extra>",
        customdata=customdata2
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

@callback(
    Output('song-info', 'children'),
    Input('scatter-plot', 'clickData')
)
def display_song_info(clickData):
    if clickData:
        point = clickData['points'][0]['customdata']
        name, artist, genre, emoji, vibe, link = point
        return html.Div([
            html.H3(f"{name} {emoji}"),
            html.P(f"Artist: {artist}"),
            html.P(f"Vibe: {vibe}"),
            html.P(f"Genre: {genre}"),
            html.A("🎧 Listen on Spotify", href=link, target="_blank", style={"color": "#ff69b4"})
        ])
    return "Click a point to see song details!"

# if __name__ == '__main__':
#     app.run(debug=True) 