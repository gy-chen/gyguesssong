import pytest


@pytest.fixture
def app():
    from gyguesssong.app import create_app
    app = create_app()
    with app.app_context():
        yield app
