import pytest

from page_analyzer.app import app


@pytest.fixture()
def client():
    return app.test_client()


def test_home_page(client):
    response = client.get('/')
    assert 'Анализатор страниц' in response.text


def test_url_page(client):
    response = client.get('/urls')
    assert 'Сайты' in response.text
