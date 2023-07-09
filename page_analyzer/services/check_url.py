import logging

from page_analyzer.models import URLChecks
from page_analyzer.services.db import PostgresDB

INSERT_CHECK_URL = """INSERT INTO
url_checks (url_id, status_code, h1, title, description, created_at)
VALUES (%s, %s, %s, %s, %s, %s);"""


class CheckURLService:

    def __init__(self, db: PostgresDB):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def check(self, url_id):
        result = self.check_url(url_id)
        if result:
            self.db.execute_query(INSERT_CHECK_URL, (
                result.url_id,
                result.status_code,
                result.h1,
                result.title,
                result.description,
                result.created_at,
            ), commit=True)
            return 'Страница успешно проверена', 'success'
        return 'Произошла ошибка при проверке', 'danger'

    @staticmethod
    def check_url(url_id):
        return URLChecks(url_id=url_id)
