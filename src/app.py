"""
Main script: execute to start the server
"""


import logging
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import flask
import flask_monitoringdashboard
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import dash
import src.config
from dash.dependencies import Input, Output
from src import __config, config
from src.dash import figure as dash_figure

# - Create Flask and Dash apps, and fuse them with a middleware
flask_app = flask.Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=flask_app,
    # meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=0.95'}],
    external_stylesheets=["../static/css/awesome-ds.css"],
    url_base_pathname="/_dash/",
)
dash_app.layout = dash_figure.generate_layout()
app = DispatcherMiddleware(flask_app, {"/dash": dash_app.server})


# - Add a monitoring dashboard for the Flask app
flask_monitoringdashboard.config.link = __config.dashboard_link
flask_monitoringdashboard.config.username = __config.dashboard_username
flask_monitoringdashboard.config.password = __config.dashboard_password
flask_monitoringdashboard.config.guest_username = __config.dashboard_guest_username
flask_monitoringdashboard.config.guest_password = __config.dashboard_guest_password
flask_monitoringdashboard.config.database_name = __config.dashboard_database_name
flask_monitoringdashboard.bind(flask_app)


# - Configure logging
logger = logging.getLogger("waitress")
logger.handlers.clear()
logger.propagate = False
logging_path = Path(config.logging_fpath)
logging_path.parent.mkdir(exist_ok=True)
formatter = logging.Formatter(config.logging_format, datefmt=config.logging_datefmt)
formatter.converter = time.gmtime  # type: ignore
sh = logging.StreamHandler()
sh.setFormatter(formatter)
fh = RotatingFileHandler(
    config.logging_fpath,
    mode="a",
    maxBytes=config.logging_maxbytes,
    backupCount=config.logging_backups,
)
fh.setFormatter(formatter)
logger.addHandler(sh)
logger.addHandler(fh)
logger.setLevel(config.logging_level)

if config.pushover_on:
    from notifiers.logging import NotificationHandler

    ph = NotificationHandler(
        "pushover",
        defaults=dict(
            user=__config.pushover_user,
            token=__config.pushover_token,
        ),
        level=config.pushover_level,
    )
    logger.addHandler(ph)

flask_app.logger.propagate = False
flask_app.logger.handlers = logger.handlers
flask_app.logger.setLevel(logger.level)


# - Define endpoints
@dash_app.callback(Output("brownian-motion-plot", "figure"), [Input("clock", "n_intervals")])
def update_graph_scatter(_):
    return dash_figure.get_figure()


@dash_app.callback(
    Output("change-lines-button", "children"), [Input("change-lines-button", "n_clicks")]
)
def change_color_graph_scatter(n_clicks):
    from src import config

    if config.plot_n_lines <= 3:
        if n_clicks > 0:
            config.plot_n_lines += 1
            return "Oh no, that's too many lines. Remove ones!"
        else:
            return "I want to add a line!"
    else:
        if n_clicks > 0:
            config.plot_n_lines = max(config.plot_n_lines - 1, 0)
            return "Hmmm, on the second thought... Add it back!"
        else:
            return "I want to remove a line!"


@flask_app.route("/")
def index():
    return flask.render_template("index.html")


@flask_app.route("/cv")
def cv():
    email_name, email_domain = __config.email.split("@")
    return flask.render_template(
        "cv.html",
        email_name=email_name,
        email_domain=email_domain,
    )


if __name__ == "__main__":
    import waitress

    waitress.serve(
        app,
        host=src.config.server_host,
        port=src.config.server_port,
        threads=src.config.server_n_threads,
    )
