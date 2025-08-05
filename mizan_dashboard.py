import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

MIZAN_LEVELS_DATA = {
    "Survival & Security": {
        "positive": ["Safety", "Stability", "Security"],
        "limiting": ["Control", "Fear", "Blame"],
    },
    "Belonging & Connection": {
        "positive": ["Trust", "Respect", "Belonging"],
        "limiting": ["Judgment", "Exclusion", "Favoritism"],
    },
    "Achievement & Status": {
        "positive": ["Initiative", "Recognition", "Excellence"],
        "limiting": ["Ego", "Competition", "Status"],
    },
    "Growth & Innovation": {
        "positive": ["Learning", "Curiosity", "Creativity"],
        "limiting": ["Rigidity", "Risk Aversion", "Complacency"],
    },
    "Purpose & Integrity": {
        "positive": ["Authenticity", "Alignment", "Accountability"],
        "limiting": ["Hypocrisy", "Inconsistency", "Manipulation"],
    },
    "Service & Contribution": {
        "positive": ["Mentorship", "Support", "Giving Back"],
        "limiting": ["Martyrdom", "Burnout", "Neglect"],
    },
    "Legacy & Sustainability": {
        "positive": ["Justice", "Ethical Impact", "Stewardship"],
        "limiting": ["Neglect", "Exploitation", "Short-Termism"],
    }
}

# Assign default score to each level (you can replace with real data later)
levels = [
    {"name": name, "score": 70, "color": "#00796b"} for name in MIZAN_LEVELS_DATA.keys()
]

# Build the graph
def create_figure():
    fig = go.Figure()
    for i, lvl in enumerate(levels):
        fig.add_trace(go.Barpolar(
            r=[lvl["score"]],
            theta=[i * (360 / 7)],
            width=[360 / 7 - 5],
            marker_color=lvl["color"],
            name=lvl["name"]
        ))
    fig.update_layout(
        template="plotly_white",
        polar=dict(
            radialaxis=dict(range=[0, 100], showticklabels=False, ticks=''),
            angularaxis=dict(showticklabels=True, tickmode='array',
                             tickvals=[i * (360 / 7) for i in range(7)],
                             ticktext=[lvl["name"] for lvl in levels])
        ),
        showlegend=False
    )
    return fig

# Create Dash app
app = Dash(__name__)
app.title = "Mizan Interactive Framework"

# Layout
app.layout = html.Div([
    html.H1("Mizan 7-Level Culture Framework", style={"textAlign": "center"}),
    dcc.Graph(id="mizan-graph", figure=create_figure()),
    html.Div(id="level-insights", style={"padding": "20px", "borderTop": "1px solid #ccc"})
])

# Callback to show values when a level is clicked
@app.callback(
    Output("level-insights", "children"),
    Input("mizan-graph", "clickData")
)
def display_level_details(clickData):
    if not clickData:
        return html.P("Click on a level to explore its values.", style={"fontStyle": "italic"})

    # Use 'theta' to infer which level was clicked
    try:
        clicked_theta = clickData["points"][0]["theta"]
        index = int(round(clicked_theta / (360 / 7))) % 7
        clicked_label = levels[index]["name"]
    except Exception as e:
        return html.P(f"⚠️ Error interpreting selection: {e}")

    data = MIZAN_LEVELS_DATA.get(clicked_label, {})
    if not data:
        return html.P("No data available for this level.")

    return html.Div([
        html.H4(f"{clicked_label} – Values Overview"),
        html.Div([
            html.Strong("Positive Values: "),
            html.Span(", ".join(data.get("positive", [])))
        ]),
        html.Br(),
        html.Div([
            html.Strong("Limiting Values: "),
            html.Span(", ".join(data.get("limiting", [])))
        ])
    ], style={"background": "#f9f9f9", "padding": "15px", "borderRadius": "8px"})

# Run server
if __name__ == "__main__":
    app.run(debug=True)