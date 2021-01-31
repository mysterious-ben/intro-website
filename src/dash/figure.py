"""
Generate Dash figure
"""


import math

import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objects as go

from src import config
from src.dash.data import _get_data


def _get_traces():
    mtrx = _get_data()
    n_points = mtrx.shape[0]
    n_lines = mtrx.shape[1]
    traces = list()
    for i in range(n_lines):
        traces.append(
            go.Scatter(
                x=list(range(n_points)),
                y=mtrx[:, i],
                name="feed {}".format(i),
                mode="lines+markers",
                line=dict(width=1),
                marker=dict(size=3),
                hoverinfo="none",
            )
        )
    return traces


def get_figure():
    traces = _get_traces()
    y_lim = math.sqrt(config.plot_n_points) * config.plot_std * config.plot_y_scale
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            template="plotly_dark",
            xaxis=dict(
                range=[0, config.plot_n_points - 1],
                autorange=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-y_lim, y_lim],
                autorange=False,
                zeroline=False,
                showticklabels=False,
            ),
            showlegend=False,
            plot_bgcolor="#000",
            paper_bgcolor="#000",
            margin=dict(l=20, r=20, t=20, b=20),
        ),
    )
    return fig


def generate_layout():
    layout = html.Div(
        html.Div(
            children=[
                # html.H1("Dash app"),
                dcc.Graph(
                    id="brownian-motion-plot",
                    figure=get_figure(),
                    animate=True,
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                    },
                    style={
                        "display": "flex",
                        "flex": "2 1",
                        "flex-direction": "column",
                        "width": "99vw",
                        "max-height": "90vh",
                        "margin-top": "30px",
                        # "padding-top": "100px",
                    },
                ),
                html.Button(
                    children="Mysterious button",
                    id="change-lines-button",
                    n_clicks=0,
                    style={
                        # 'display': 'flex',
                        # 'flex': '0 1',
                        # 'flex-direction': 'column',
                        # 'min-height': '4vh',
                        "margin-bottom": "30px",
                        # "padding-bottom": "50px",
                    },
                ),
                dcc.Interval(
                    id="clock",
                    interval=config.plot_rand_seconds * 1000,
                    max_intervals=-1,
                    n_intervals=0,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "space-between",
                "align-items": "center",
                # 'text-align': 'center',
                "height": "99vh",
            },
        )
    )
    return layout
