import dash
from dash import html, dcc, Input, Output, State, callback
import pandas as pd

dash.register_page(__name__, path='/recommend')

df = pd.read_csv("cleaned_spotify_features.csv")  # Contains your clustered song features

layout = html.Div([
    html.H2("🎧 Get Song Recommendations"),
    html.P("Enter a song name or artist you like:"),
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

    # Get the first match’s cluster
    cluster = matches.iloc[0]['vibe_cluster']

    # Recommend songs in same cluster (excluding the original)
    recs = df[(df['vibe_cluster'] == cluster) & (~df['track_name'].str.contains(song_input, case=False, na=False))]
    recs = recs.sort_values('popularity', ascending=False).head(10)

    return html.Ul([html.Li(f"{row['track_name']} by {row['artist_name']}") for _, row in recs.iterrows()])