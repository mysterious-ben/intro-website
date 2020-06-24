from flask import Flask, request, jsonify, render_template

from src import config


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    import waitress
    waitress.serve(app, host=config.server_host, port=config.server_port)
