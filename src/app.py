"""
Main script: execute to start the server
"""


import flask
import dash
from dash.dependencies import Output, Input
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.dash import figure as dash_figure
from src import __config


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
    waitress.serve(app, host=__config.server_host, port=__config.server_port)



