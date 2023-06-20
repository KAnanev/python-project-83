def test_add_url(client):
    response = client.post('/', data={
        'url': 'https://www.google.com'
    })
    assert response.status_code == 200
