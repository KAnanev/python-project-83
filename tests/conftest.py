import os

import pytest
from page_analyzer import create_app
from page_analyzer.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as file:
    _test_data_sql = file.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'DATABASE_URL': 'postgresql://test_user:test_pass@localhost:5433/test_db'
        }
    )

    with app.app_context():
        db = get_db()
        init_db()
        db.execute(_test_data_sql)
        db.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
