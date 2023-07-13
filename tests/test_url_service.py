import json

from page_analyzer.models import URLSModel, URLModel
from page_analyzer.services.url import URLService
from page_analyzer.db import get_db


def test_get_json_by_id(app):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        item = url_service.get_json_by_id(1)
        assert item.id == 1
        assert isinstance(item.url_checks, list)
        assert item.url_checks

        item = url_service.get_json_by_id(2)
        assert item.id == 2
        assert isinstance(item.url_checks, list)
        assert not item.url_checks

        item = url_service.get_json_by_id(100)
        assert not item
        assert item is None

        item = url_service.get_json_by_id(0)
        assert item is None

        item = url_service.get_json_by_id(-1)
        assert item is None


def test_get_all_urls(app):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        data = url_service.get_all_urls()
        assert isinstance(data, list)
        assert isinstance(data[0], URLModel)
        assert data[0].id == 2
        assert data[1].id == 1


def test__get_url_id_by_url_name(app):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        item = URLModel(name='https://chatbot.theb.ai')
        data = url_service.get_url_id_by_url_name(item)
        assert not data.id

        item = URLModel(name='http://www.ya.ru/')
        data = url_service.get_url_id_by_url_name(item)
        assert data.id


def test_insert_item(app, client):
    with app.app_context():
        db = get_db()
        url_service = URLService(db=db)
        result = url_service.insert_url('http://www.ya.ru/')
        assert result['item'].name == 'http://www.ya.ru'
        assert result['message'] == ('Страница уже существует', 'info')

        result = url_service.insert_url('https://pythonist.ru/python-map-znakomstvo/')
        assert result['item'].name == 'https://pythonist.ru'
        assert result['message'] == ('Страница успешно добавлена', 'success')

        result = url_service.insert_url('htp://ya.ru')
        assert result['item'] is None
        assert result['message'] == ('Некорректный URL', 'danger')
