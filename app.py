# imports
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback,  dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# read file
dirpath = os.getcwd()
file_dir = os.path.join(dirpath, "data", "out_gaus_simple")
file_dict = [{'label': "_".join(file.split("_")[:5]), "value": file} for file in os.listdir(file_dir)]
q_dict = [{'label': '1', 'value': 1},{'label': '2', 'value': 2},{'label': '3', 'value': 3},{'label': '4', 'value': 4}]

def filter_df(input_dir, file, q):
    filepath = os.path.join(input_dir, file)
    file = np.loadtxt(filepath, delimiter = ",")
    idx = np.where(file[:, 5] == q)[0]
    df2 = file[idx, :]
    return df2

def make_plot(all_points):
    points = all_points[:, [0, 1, 2]]
    fig = go.Figure(data=[go.Scatter3d(x = points[:, 0], y = points[:, 1], z=points[:, 2], mode='markers', marker=dict(size=2, color="gray", opacity=0.8), name = "raw")])
    points = all_points[:, [0, 1, 3]]
    fig.add_trace(go.Scatter3d(x = points[:, 0], y = points[:, 1], z=points[:, 2], mode='markers', marker=dict(color="red", size = 2), name = "teat", visible='legendonly'))
    points = all_points[:, [0, 1, 4]]
    fig.add_trace(go.Scatter3d(x = points[:, 0], y = points[:, 1], z=points[:, 2], mode='markers', marker=dict(color="blue", size = 2), name = "udder"))

    fig.update_layout(paper_bgcolor="black", font_color = "white", plot_bgcolor = "black", width=750, height=500)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    fig.update_layout(scene_aspectmode='data')
    return fig


def blank_fig():
    fig = go.Figure(go.Scatter3d(x=[], y = [], z=[]))
    fig.update_layout(paper_bgcolor="black")
    fig.update_layout(legend_font_color="white", width=750, height=500)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    return fig

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

MENU_STYLE = {
    'backgroundColor': 'black',
    'color': 'white',
}

sidebar = html.Div(
    [
        html.H2("Udder", className="display-4"),
        html.Hr(),
        html.P(
            "choose a cow", className="lead"
        ),
        html.Label("Q:"),
        dcc.RadioItems(id = 'q-btn', options=q_dict, value=1),
        
        html.Label("Cow ID:"),
        dcc.Dropdown(id='cows-dpdn',options= file_dict, value = '1023_20231117_124217_frame_100_udder.csv', style = MENU_STYLE),

    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
[html.Div(
             [dbc.Row(
                [dbc.Col([dcc.Graph(id='graph1', figure = blank_fig())]), 
                 dbc.Col([dcc.Graph(id='graph2', figure = blank_fig())])]), 
              dbc.Row(
                [dbc.Col([dcc.Graph(id='graph3', figure = blank_fig())]), 
                 dbc.Col([dcc.Graph(id='graph4', figure = blank_fig())])])])
], id="page-content", style=CONTENT_STYLE)

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
server = app.server

@app.callback(
    Output("graph2", "figure"),
    Input('cows-dpdn', 'value'), 
    Input('q-btn', 'value'))
def get_frames(filename, q):
    global dirpath
    input_dir = os.path.join(dirpath, "data", "out_gaus_simple")
    points_filtered = filter_df(input_dir, filename, q)
    print(len(points_filtered))
    fig = make_plot(points_filtered)
    fig.update_layout(title=dict(text="Gauss simple", font=dict(size=20)))
    return fig

@app.callback(
    Output("graph1", "figure"),
    Input('cows-dpdn', 'value'), 
    Input('q-btn', 'value'))
def get_frames(filename, q):
    global dirpath
    input_dir = os.path.join(dirpath, "data", "out_gaus")
    points_filtered = filter_df(input_dir, filename, q)
    print(len(points_filtered))
    fig = make_plot(points_filtered)
    fig.update_layout(title=dict(text="Gauss old", font=dict(size=20)))
    return fig

@app.callback(
    Output("graph3", "figure"),
    Input('cows-dpdn', 'value'), 
    Input('q-btn', 'value'))
def get_frames(filename, q):
    global dirpath
    input_dir = os.path.join(dirpath, "data", "out_splines")
    points_filtered = filter_df(input_dir, filename, q)
    print(len(points_filtered))
    fig = make_plot(points_filtered)
    fig.update_layout(title=dict(text="Splines", font=dict(size=20)))
    return fig

if __name__ == '__main__':
    app.run(debug=True)