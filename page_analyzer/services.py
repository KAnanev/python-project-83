from datetime import datetime
from urllib.parse import urlparse, urlunparse
import validators


LEN_URL = 255


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
