"""
Main script: execute to start the server
"""

#TODO: network activity logging
#TODO: notification on error
#TODO: [optional] CPU/RAM monitoring
#TODO: [optional] font: helvica
#TODO: hide "see profile"


import flask
import dash
from dash.dependencies import Output, Input
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import src.config
from src.dash import figure as dash_figure
from src import __config
from src import config


import logging
from logging.handlers import RotatingFileHandler
import time
from pathlib import Path
logger = logging.getLogger('waitress')
logger.handlers.clear()
logger.propagate = False
logging_path = Path(config.logging_fpath)
logging_path.parent.mkdir(exist_ok=True)
formatter = logging.Formatter(config.logging_format, datefmt=config.logging_datefmt)
formatter.converter = time.gmtime
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(config.logging_level)
fh = RotatingFileHandler(config.logging_fpath, mode='a', maxBytes=config.logging_maxbytes, backupCount=config.logging_backups)
fh.setFormatter(formatter)
fh.setLevel(config.logging_level)
logger.addHandler(sh)
logger.addHandler(fh)


flask_app = flask.Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=flask_app,
    # meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=0.95'}],
    external_stylesheets=['../static/css/awesome-ds.css'],
    url_base_pathname='/_dash/',
)
dash_app.layout = dash_figure.generate_layout()
app = DispatcherMiddleware(flask_app, {'/dash': dash_app.server})


@dash_app.callback(Output('brownian-motion-plot', 'figure'),
                   [Input('clock', 'n_intervals')])
def update_graph_scatter(_):
    return dash_figure.get_figure()


@dash_app.callback(Output('change-lines-button', 'children'),
                   [Input('change-lines-button', 'n_clicks')])
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
            config.plot_n_lines = max(config.plot_n_lines-1, 0)
            return "Hmmm, on the second thought... Add it back!"
        else:
            return "I want to remove a line!"


@flask_app.route('/')
def index():
    return flask.render_template('index.html')


@flask_app.route('/cv')
def cv():
    email_name, email_domain = __config.email.split('@')
    return flask.render_template(
        'cv.html',
        xmlparser_project_link=__config.xmlparser_project_link,
        website_project_link=__config.website_project_link,
        sales_project_link=__config.sales_project_link,
        titanic_project_link=__config.titanic_project_link,
        toptal_profile_link=__config.toptal_profile_link,
        linkedin_profile_link=__config.linkedin_profile_link,
        github_profile_link=__config.github_profile_link,
        email_name=email_name,
        email_domain=email_domain,
    )


if __name__ == '__main__':
    import waitress
    waitress.serve(app, host=src.config.server_host, port=src.config.server_port, threads=src.config.server_n_threads)

