from typing import List, Optional

from page_analyzer.models import URLModel, URLSModel
from page_analyzer.services.db import PostgresDB
from page_analyzer.services.sql_query import (
    GET_ITEMS,
    GET_JSON_BY_ID,
    GET_JSON_BY_URL,
    INSERT_ITEM_RETURN_JSON
)


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
            items = [URLSModel(**item['result']) for item in sorted_items]
        return items

    def get_url_id_by_url_name(self, item: URLModel) -> Optional[URLModel]:

        exist_item = self.db.execute_query(GET_JSON_BY_URL, (item.name,), )
        if exist_item:
            item = URLModel(**exist_item['result'])
        return item

    def insert_url(self, url: str) -> dict[str, tuple[str, str] | URLModel]:

        item = None

        try:
            item = URLModel(name=url)
            item = self.get_url_id_by_url_name(item)

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
