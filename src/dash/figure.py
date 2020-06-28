import math
import numpy as np
from plotly import graph_objects as go
import dash_html_components as html
import dash_core_components as dcc

from src import config


def _get_data():
    dx = np.random.normal(0, config.std, config.n_points * config.n_lines).reshape(config.n_points, config.n_lines)
    dx[0, :] = 0
    x = np.cumsum(dx, axis=0)
    return x


def _get_traces():
    mtrx = _get_data()
    n_points = mtrx.shape[0]
    n_lines = mtrx.shape[1]
    traces = list()
    for i in range(n_lines):
        traces.append(go.Scatter(
            x=list(range(n_points)),
            y=mtrx[:, i],
            name='feed {}'.format(i),
            mode='lines+markers',
            line=dict(width=1),
            marker=dict(size=3),
            hoverinfo='none',
        ))
    return traces


def get_figure():
    traces = _get_traces()
    y_lim = math.sqrt(config.n_points) * config.std * config.yaxis_factor
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            template='plotly_dark',
            xaxis=dict(range=[0, config.n_points - 1], autorange=False, zeroline=False, showticklabels=False),
            yaxis=dict(
                range=[-y_lim, y_lim],
                autorange=False, zeroline=False, showticklabels=False,
            ),
            showlegend=False,
            plot_bgcolor='#000',
            paper_bgcolor='#000',
            margin=dict(l=20, r=20, t=20, b=20),
        )
    )
    return fig


def generate_layout():
    layout = html.Div(
        html.Div(children=[
            # html.H1("Dash app"),
            dcc.Graph(
                id='brownian-motion-plot', figure=get_figure(), animate=True,
                config={
                    'displayModeBar': False,
                    'scrollZoom': False,
                },
                style={'height': '95vh'},
            ),
            dcc.Interval(id='clock', interval=1 * 1000, max_intervals=-1, n_intervals=0),
            ],
        )
    )
    return layout
