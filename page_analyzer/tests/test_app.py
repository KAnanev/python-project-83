import pytest

from page_analyzer.app import app


@pytest.fixture()
def client():
    return app.test_client()


def test_home_page(client):
    response = client.get('/')
    assert '<h1>Анализатор страниц</h1>' in response.text
