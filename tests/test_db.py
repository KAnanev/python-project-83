import psycopg
import pytest

from page_analyzer.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(psycopg.OperationalError) as error:
        db.execute_query('SELECT 1')

    assert 'closed' in str(error.value)


def test_get_data_db(app):
    with app.app_context():
        db = get_db()

        result = db.execute_query('select * from urls;')
        assert isinstance(result, dict)

        result = db.execute_query('select * from urls;', many=True)
        assert isinstance(result, list)
