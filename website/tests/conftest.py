from website import app
import pytest


@pytest.fixture
def client():
    app.debug = True
    app.config.from_object({"TESTING": True})
    with app.test_client() as client:
        yield client
