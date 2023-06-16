import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL=os.getenv('DATABASE_URL')
    )

    if test_config:
        app.config.from_mapping(test_config)

    from page_analyzer.db import init_app
    init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/urls')
    def urls():
        return render_template('urls.html')

    return app
