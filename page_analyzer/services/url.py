from urllib.parse import urlparse

import validators

from typing import Dict, Any, List
from psycopg import Connection

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
    def __init__(self, db: Connection[Dict[str, Any]]):
        self.db = db

    @staticmethod
    def validate_url(url: str):
        return all(
            [
                validators.url(url), validators.length(url, max=URL_MAX_LENGTH)
            ]
        )

    @staticmethod
    def normalize_url(url: str):
        url = urlparse(url)
        return f'{url.scheme}://{url.netloc}'.lower()

    def _get_item_by_url(self, url: str) -> Dict[str, Any] | None:
        item = self.db.execute(
            GET_ITEM_BY_URL,
            (self.normalize_url(url),)
        ).fetchone()
        return item

    def get_item_by_id(self, url_id: int) -> Dict[str, Any] | None:
        item = self.db.execute(GET_ITEM_BY_ID_, (url_id,)).fetchall()
        if not item:
            return None
        return item

    def get_all_items(self) -> List[Dict[str, Any]] | None:
        items = self.db.execute(GET_ITEMS).fetchall()
        if not items:
            return None
        return sorted(items, key=lambda x: -x['id'])

    def insert_item(self, url: str) -> Dict[str, Any]:

        result = {
            'item': None,
            'message': ('Некорректный URL', 'danger')
        }

        if self.validate_url(url):
            result['item'] = self._get_item_by_url(self.normalize_url(url))
            result['message'] = ('Страница уже существует', 'info')

            if not result['item']:
                result['item'] = self.db.execute(
                    INSERT_ITEM,
                    (
                        self.normalize_url(url),
                        get_date_now()
                    )
                ).fetchone()
                self.db.commit()
                result['message'] = ('Страница успешно добавлена', 'success')

        return result

    def check_url(self, url_id: int) -> Dict[str, Any]:
        item = self.get_item_by_id(url_id)
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
        self.db.execute(
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
        self.db.commit()
        return 'Страница успешно добавлена', 'success'
