import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()


def create_app(test_config=None):
    _app = Flask(__name__)
    _app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE_URL=os.getenv('DATABASE_URL')
    )

    if test_config:
        _app.config.from_mapping(test_config)

    from page_analyzer.db import init_app
    init_app(_app)

    from page_analyzer import views
    _app.register_blueprint(views.bp)
    _app.add_url_rule('/', endpoint='index')

    return _app


app = create_app()
