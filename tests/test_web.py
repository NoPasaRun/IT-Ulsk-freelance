from pathlib import Path

import pytest
from app import create_app


ROUTES = [
    "/", "/news", "/news-detail", "/companies",
    "/ratings", "/company-detail/1", "/eco-system",
    "/event-detail/1"
]
root = Path(".").parent.parent


@pytest.fixture()
def app():
    test_app = create_app(root / "static", root / "templates")
    test_app.config.update({
        "TESTING": True
    })

    yield test_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.mark.parametrize("route", ROUTES)
def test_content_access(client, route: str):
    response = client.get(route)
    assert any([str(response.status_code).startswith(code) for code in ["2", "3"]])
