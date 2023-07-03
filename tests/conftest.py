import os

import pytest

from dotenv import load_dotenv
from page_analyzer import create_app
from page_analyzer.db import init_db, get_db

load_dotenv()

with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as file:
    _test_data_sql = file.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'DATABASE_URL': os.getenv('TEST_DATABASE_URL'),
            'SECRET_KEY': os.getenv('SECRET_KEY'),
        }
    )

    with app.app_context():
        db = get_db()
        init_db()
        db.execute_query(_test_data_sql)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
