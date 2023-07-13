def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '<a class="navbar-brand" href="/">Анализатор страниц</a>' in response.text
    assert '<a class="nav-link " href="/urls">Сайты</a>' in response.text
    assert '<form action="/urls" method="post" ' in response.text
    assert '<input type="text" name="url"' in response.text


def test_urls(client):
    response = client.get('/urls')
    assert response.status_code == 200
    assert 'data-test="urls"' in response.text
    assert 'http://www.ya.ru' in response.text
    assert 'http://www.google.ru' in response.text


def test_url(client):
    response = client.get('/urls/1')
    assert 'http://www.ya.ru' in response.text
    assert '1' in response.text
    assert 'data-test="checks"' in response.text

    response = client.get('/urls/2')
    assert 'http://www.google.ru' in response.text
    assert '2' in response.text


def test_post_url_valid_url(client):

    response = client.post('/urls', data={
        'url': 'https://habr.com'
    }, follow_redirects=True)
    assert 'Страница успешно добавлена' in response.text

    response = client.post('/urls', data={
        'url': 'https://yandex.ru'
    })
    assert response.status_code == 302
    assert '/urls/4' in response.location


def test_post_url_exist(client):

    response = client.post('/urls', data={
        'url': 'https://habr.com'
    })
    assert response.status_code == 302
    assert response.location == '/urls/3'

    response = client.post('/urls', data={
        'url': 'https://habr.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Страница уже существует' in response.text


def test_post_url_invalid_url(client):
    response = client.post('/urls', data={
        'url': 'htps://habr.com'
    })
    assert response.location == '/'

    response = client.post('/urls', data={
        'url': 'htps://habr.com'
    }, follow_redirects=True)
    assert 'Некорректный URL' in response.text


def test_post_url_check(client):
    response = client.post('/urls/1/checks')

    assert response.status_code == 302
    assert response.location == '/urls/1'

    response = client.post('/urls/1/checks', follow_redirects=True)
    assert '5' in response.text
    assert '200' in response.text

    response = client.post('/urls/1/checks', follow_redirects=True)
    assert '6' in response.text

    response = client.post('/urls/2/checks', follow_redirects=True)
    assert '7' in response.text
