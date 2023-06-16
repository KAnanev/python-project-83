def test_home_page(client):
    response = client.get('/')
    assert 'Анализатор страниц' in response.text


def test_url_page(client):
    response = client.get('/urls')
    assert 'Сайты' in response.text
