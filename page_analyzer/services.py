from datetime import datetime
from urllib.parse import urlparse
import validators
from flask import flash


LEN_URL = 255
SELECT_URL_QUERY = 'SELECT * FROM urls WHERE name = (%s)'
INSERT_URL_QUERY = 'INSERT INTO urls (name, created_at) ' \
                   'VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING id'


def get_date_now():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


class URLParse:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)

    @property
    def validate(self):
        return all(
            [
                validators.url(self.url), validators.length(self.url, max=255)
            ]
        )

    @property
    def normalize(self):
        return f'{self.parsed_url.scheme}://{self.parsed_url.netloc}'.lower()


def check_url(normalized_url, db):
    """Функция чекает урл в базе и если есть возвращает его id"""

    url_id = None

    try:
        url_id = db.execute(
            SELECT_URL_QUERY, (normalized_url,)
        ).fetchone()['id']
    except TypeError:
        pass
    return url_id


def add_or_get_url(normalized_url, db):
    """Добвляем урл или возвращаем его id"""

    url_id = check_url(normalized_url, db)

    if url_id:
        flash('Страница уже существует', 'info')
    else:
        url_id = db.execute(
            INSERT_URL_QUERY, (normalized_url, get_date_now())
        ).fetchone()['id']
        db.commit()
        flash('Страница успешно добавлена', 'success')
    return url_id
