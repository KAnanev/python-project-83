import pytest
from page_analyzer import app


@pytest.fixture()
def client():
    return app.test_client()
