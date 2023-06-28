from urllib.parse import urlparse

import validators

from typing import Dict, Any, List
from psycopg import Connection

from page_analyzer.services.utils import get_date_now

GET_ITEMS = 'SELECT * FROM urls'
GET_ITEM_BY_ID = 'SELECT * FROM urls WHERE id = (%s)'
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

    def get_by_id(self, url_id: int) -> Dict[str, Any] | None:
        item = self.db.execute(GET_ITEM_BY_ID, (url_id,)).fetchone()
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
