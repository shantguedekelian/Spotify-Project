from dash import html, dcc
from app import app
import dash

app.layout = html.Div([
    html.H1("🎶 Song Explorer"),
    html.Div([
        dcc.Link("🔍 Mood Explorer", href="/"),
        html.Span(" | "),
        dcc.Link("🎧 Song Recommender", href="/recommend"),
    ]),
    html.Hr(),
    dash.page_container  # Displays the current page content
])

if __name__ == "__main__":
    app.run(debug=True)