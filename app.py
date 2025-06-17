import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load and prepare data
df = pd.read_csv("cleaned_spotify_features.csv")

#Setting up dash app
app = dash.Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div([
    html.H1("Spotify Dashboard"),
    
    html.Div([
        dcc.Link("🏠 Home", href="/", style={'margin': '10px'}),
        dcc.Link("🔍 Recommender", href="/recommend", style={'margin': '10px'}),
    ], style={'marginBottom': '20px'}),
    
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)
