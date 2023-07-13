import logging

import requests

from page_analyzer.services.url import URLService
from bs4 import BeautifulSoup
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

    def check_url(self, url_id):
        url_service = URLService(self.db)
        url = url_service.get_json_by_id(url_id).name
        if url:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            h1_tag = soup.find('h1').text if soup.find('h1') else None
            title = soup.find('title').text if soup.find('title') else None
            description_tag = soup.find('meta', attrs={'name': 'description'})

            description = description_tag[
                'content'] if description_tag else None
            if response:
                return URLChecks(
                    url_id=url_id,
                    status_code=response.status_code,
                    h1=h1_tag,
                    title=title,
                    description=description,
                )
