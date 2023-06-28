from page_analyzer.services.url import URLService
from page_analyzer.db import get_db


def test__get_id_by_url(app):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        data = url_service._get_item_by_url(url_service.normalize_url('https://chatbot.theb.ai/'))
        assert data is None

        data = url_service._get_item_by_url(url_service.normalize_url('http://www.ya.ru/'))
        assert isinstance(data, dict)


def test_get_item(app):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        data = url_service.get_by_id(1)
        assert data['id'] == 1

        data = url_service.get_by_id(100)
        assert data is None


def test_get_items(app):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        items = url_service.get_all_items()
        assert len(items) == 2
        assert items[0]['id'] == 2
        assert items[1]['id'] == 1


def test_insert_item(app, client):
    with app.app_context():
        with app.test_client() as client:
            db = get_db()
            url_service = URLService(db=db)
            result = url_service.insert_item('http://www.ya.ru/')
            assert result['item']['name'] == 'http://www.ya.ru'

            result = url_service.insert_item('http://www.ya.ru')
            assert result['item']['name'] == 'http://www.ya.ru'

            result = url_service.insert_item('htp://ya.ru')
            assert result['item'] is None
