import pytest

from page_analyzer.app import app


@pytest.fixture()
def client():
    return app.test_client()


def test_home_page(client):
    response = client.get('/')
    assert b'Hello, world!' in response.data
    assert b'Buy, world!' not in response.data
