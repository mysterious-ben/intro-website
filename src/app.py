import flask
import dash
from dash.dependencies import Output, Input
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.dash import figure as dash_figure
from src import config


flask_app = flask.Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=flask_app,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
    external_stylesheets=['../static/css/awesome-ds.css'],
    url_base_pathname='/_dash/',
)
dash_app.layout = dash_figure.generate_layout()
app = DispatcherMiddleware(flask_app, {'/dash': dash_app.server})


@dash_app.callback(Output('brownian-motion-plot', 'figure'),
                   [Input('clock', 'n_intervals')])
def update_graph_scatter(_):
    return dash_figure.get_figure()


@flask_app.route('/')
def index():
    return flask.render_template('index.html', graphics='placeholder')


if __name__ == '__main__':
    import waitress
    waitress.serve(app, host=config.server_host, port=config.server_port)



