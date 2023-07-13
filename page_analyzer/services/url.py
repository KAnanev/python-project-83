from typing import List, Optional

from page_analyzer.models import URLModel, URLSModel
from page_analyzer.services.db import PostgresDB

GET_ITEMS = """SELECT
     json_build_object(
            'id', id,
            'name', name,
            'created_at', created_at
) AS result
FROM urls;"""

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

GET_JSON_BY_URL = """SELECT
    json_build_object(
        'id', id,
        'name', name,
        'created_at', created_at
) AS result
FROM urls WHERE name = (%s)"""

INSERT_ITEM_RETURN_JSON = """INSERT INTO
    urls (name, created_at)
    VALUES (%s,%s)
    RETURNING json_build_object(
        'id', id,
        'name', name,
        'created', created_at
    ) AS result;"""


class URLService:
    def __init__(self, db: PostgresDB):
        self.db = db

    def get_json_by_id(self, url_id: int) -> Optional[URLSModel]:
        item = self.db.execute_query(GET_JSON_BY_ID, (url_id,), )
        if not item:
            return None
        return URLSModel(**item['result'])

    def get_all_urls(self) -> List[URLModel] | None:
        items = self.db.execute_query(GET_ITEMS, many=True)
        if items:
            sorted_items = sorted(items, key=lambda item: -item['result']['id'])
            items = [URLModel(**item['result']) for item in sorted_items]
        return items

    def _get_url_id_by_url_name(self, item: URLModel) -> Optional[URLModel]:

        exist_item = self.db.execute_query(GET_JSON_BY_URL, (item.name,), )
        if exist_item:
            item = URLModel(**exist_item['result'])
        return item

    def insert_url(self, url: str) -> dict[str, tuple[str, str] | URLModel]:

        item = None

        try:
            item = URLModel(name=url)
            item = self._get_url_id_by_url_name(item)

            if item.id:
                message = ('Страница уже существует', 'info')

            else:
                raw_item = self.db.execute_query(
                    INSERT_ITEM_RETURN_JSON,
                    (item.name, item.created_at),
                    commit=True
                )
                item = URLModel(**raw_item['result'])
                message = ('Страница успешно добавлена', 'success')
        except ValueError:
            message = ('Некорректный URL', 'danger')

        return {
            'item': item,
            'message': message,
        }
