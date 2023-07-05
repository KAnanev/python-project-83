from urllib.parse import urlparse

import validators
from page_analyzer.models import URLModel, URLSModel
from typing import Dict, Any, List, Optional
from psycopg import Connection

from page_analyzer.services.db import PostgresDB
from page_analyzer.services.utils import get_date_now

GET_ITEMS = 'SELECT * FROM urls'
GET_ITEM_BY_ID = '''
SELECT 
urls.id as url_id, urls.name as url_name, urls.created_at as url_created_at,
url_checks.id as url_check_id, url_checks.status_code as url_check_status_code,
url_checks.h1 as  url_check_h1, 
url_checks.title as url_check_title, url_checks.description as url_check_description, 
url_checks.created_at as url_check_created_at
FROM urls 
LEFT JOIN url_checks ON urls.id = url_checks.url_id
WHERE urls.id = (%s)
'''

GET_JSON_BY_ID = """SELECT 
    json_build_object(
        'id', urls.id,
        'name', urls.name,
        'created_at', urls.created_at,
        'url_checks', COALESCE(json_agg(json_build_object(
            'id', url_checks.id,
            'url_id', url_checks.url_id,
            'status_code', url_checks.status_code,
            'h1', url_checks.h1,
            'title', url_checks.title,
            'description', url_checks.description,
            'created_at', url_checks.created_at
        )) FILTER (WHERE url_checks.id IS NOT NULL) , '[]'::json)
    ) AS result
FROM urls 
LEFT JOIN url_checks ON urls.id = url_checks.url_id
WHERE urls.id = (%s)
GROUP BY urls.id;"""

GET_ITEM_BY_ID_ = '''
SELECT 
urls, url_checks
FROM urls 
LEFT JOIN url_checks ON urls.id = url_checks.url_id
WHERE urls.id = (%s)
'''

GET_ITEM_BY_URL = 'SELECT * FROM urls WHERE name = (%s)'
INSERT_ITEM = 'INSERT INTO urls (name, created_at) ' \
              'VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING id'
URL_MAX_LENGTH = 255


class URLService:
    def __init__(self, db: PostgresDB):
        self.db = db

    def get_json_by_id(self, url_id: int):
        item = self.db.execute_query(GET_JSON_BY_ID, (url_id,), )
        if not item:
            return None
        return item

    def _get_url_by_name(self, url: URLModel) -> list[Any] | None:
        item = self.db.execute_query(GET_ITEM_BY_URL, (url.name,), )
        if not item:
            return None
        return item

    def get_url_by_id(self, url_id: int) -> Dict[str, Any] | None:
        item = self.db.execute_query(GET_ITEM_BY_ID_, (url_id,))

        return item

    def get_all_urls(self) -> List[Dict[str, Any]] | None:
        items = self.db.execute_query(GET_ITEMS)
        if items:
            items = sorted(items, key=lambda x: -x['id'])
        return items

    def insert_url(self, url: URLModel) -> Dict[str, Any]:
        result = {
            'item': self._get_url_by_name(url),
            'message': ('Страница уже существует', 'info')
        }

        if not result['item']:
            result['item'] = self.db.execute_query(INSERT_ITEM, (url.name, get_date_now()), commit=True)
            result['message'] = ('Страница успешно добавлена', 'success')

        return result

    def check_url(self, url_id: int) -> Dict[str, Any]:
        item = self.get_url_by_id(url_id)
        ctx = {
            'url_id': item['url_id'],
            'status_code': '',
            'h1': '',
            'title': '',
            'description': '',
            'created_at': get_date_now(),
        }
        return ctx

    def insert_item_in_url_checks(self, url_id: int):
        check_url = self.check_url(url_id)
        self.db.execute_query(
            '''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
            VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s, %(created_at)s);
            ''',
            {
                'url_id': check_url['url_id'],
                'status_code': check_url['status_code'],
                'h1': check_url['h1'],
                'title': check_url['title'],
                'description': check_url['description'],
                'created_at': check_url['created_at'],

            }
        )
        return 'Страница успешно добавлена', 'success'
