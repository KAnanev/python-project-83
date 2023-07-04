import pytest
from pydantic_core._pydantic_core import ValidationError

from page_analyzer.models import URLModel, URLSModel


valid_url = (
    'https://www.google.com/',
    'https://www.amazon.com/',
    'https://github.com/',
    'https://en.wikipedia.org/',
    'https://www.apple.com/'
)

invalid_url = (
    'htp://www.google.com',  # некорректный протокол
    'https:/amazon.com',  # неправильная структура домена
    #   'https://github.com?user=me',  # неправильно закодированный параметр запроса
    'https:en.wikipedia.org',  # неверный формат протокола и домена
    '//www.apple.com/',  # отсутствует протокол
    'https://www.example.com/path with spaces',  # неправильно закодированный путь
    'https://www.example.com/search?category=electronics&subcategory=televisions&manufacturer=samsung&model'
    '=UE55RU7100UXXU&year=2021&resolution=3840x2160&picture_quality=4k&smart_features=true&connectivity'
    '=wifi_ethernet_bluetooth_hdmi_usb_av&price_min=500&price_max=1000&discount_percentage=10&sort_order=price_asc'
    '&pagination_offset=10000&session_id'
    '=abcdef1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuv'
    'wxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnopqrstuvwxyz'
    '1234567890abcdefghijk',  # правилный урл длиной больше 255
)


def func_url_parse(url):
    url_parse = URLModel(name=url)
    return url_parse


@pytest.mark.parametrize('url', valid_url)
def test_valid_url_model_parse(url):
    assert func_url_parse(url)


@pytest.mark.parametrize('url', invalid_url)
def test_invalid_url_model_parse(url):
    with pytest.raises(ValidationError):
        assert not func_url_parse(url)


def test_model_urls_parse():
    valid_data = {'id': '1', 'created_at': '2023-07-04 10:07:29', 'name': 'https://www.google.com/'}
    URLSModel(**valid_data)
    valid_data = {'created_at': '2023-07-04 10:07:29', 'name': 'https://www.google.com/'}
    URLSModel(**valid_data)
    valid_data = {'name': 'https://www.google.com/'}
    URLSModel(**valid_data)




