import flask

from src import config


app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html', graphics='placeholder')


if __name__ == '__main__':
    import waitress
    waitress.serve(app, host=config.server_host, port=config.server_port)
