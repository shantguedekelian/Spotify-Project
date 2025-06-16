import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load and prepare data
df = pd.read_csv("cleaned_spotify_features.csv")

#Setting up dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🎵 Song Explorer by Mood"),

    html.Label("Filter by Vibe:"),
    dcc.Dropdown(
        options=[{'label': vibe, 'value': vibe} for vibe in df['vibe_cluster'].unique()],
        value=None,
        id='vibe-filter',
        multi=True
    ),

    html.Label("Search by Genre:"),
    dcc.Input(id='genre-input', type='text', placeholder='e.g. pop, rap'),

    dcc.Graph(id='scatter-plot'),
    
    html.H3("Top 10 Songs by Popularity"),
    html.Div(id='top-songs'),

    html.Div(id='song-details', style={'marginTop': 20})
    
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Output('top-songs', 'children'),
    Input('vibe-filter', 'value'),
    Input('genre-input', 'value')
)
def update_plot(selected_vibes, genre_text):
    filtered_df = df.copy()

    # Filter by vibe
    if selected_vibes:
        filtered_df = filtered_df[filtered_df['vibe_cluster'].isin(selected_vibes)]

    # Filter by genre
    if genre_text:
        filtered_df = filtered_df[filtered_df['genre'].str.contains(genre_text, case=False, na=False)]

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
        html.Li(f"{row['track_name']} by {row['artist_name']} (Popularity: {row['popularity']})")
        for _, row in top_songs.iterrows()
    ])

    return fig, top_songs_table

if __name__ == '__main__':
    app.run(debug=True) 