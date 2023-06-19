from datetime import datetime
from urllib.parse import urlparse


LEN_URL = 255


def get_date_now():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


class URLParse:
    def __init__(self, url):
        self.url = url

    @property
    def validate(self):
        try:
            result = urlparse(self.url)
            return all([
                result.scheme,
                result.netloc,
                len(result) <= LEN_URL
            ])
        except ValueError:
            return False

    @property
    def normalize(self):
        parsed_url = urlparse(self.url)
        return parsed_url.netloc.lower()
