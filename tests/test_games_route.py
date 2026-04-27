import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.auth import generate_token
from app.models import User


@pytest.fixture
def client():
    with tempfile.TemporaryDirectory() as temp_dir:
        auth_db_path = os.path.join(temp_dir, "auth.sqlite")

        app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{auth_db_path}",
        })

        with app.app_context():
            db.create_all(bind_key=[None])

            yield app.test_client()

            db.session.remove()
            db.drop_all(bind_key=[None])

            for engine in db.engines.values():
                engine.dispose()


@pytest.fixture
def auth_header(client):
    with client.application.app_context():
        user = User(
            name="Test User",
            email="test@example.com",
        )
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id)

    return {"Authorization": f"Bearer {token}"}


def test_get_games_requires_name_param(client, auth_header):
    response = client.get("/api/games", headers=auth_header)

    assert response.status_code == 400
    assert response.get_json() == {"error": "The 'name' parameter is required"}


def test_get_games_returns_results_for_valid_name(client, auth_header):
    response = client.get("/api/games?name=portal", headers=auth_header)

    assert response.status_code == 200

    data = response.get_json()
    assert "count" in data
    assert "results" in data
    assert isinstance(data["results"], list)

    if data["results"]:
        first_game = data["results"][0]
        assert "appid" in first_game
        assert "name" in first_game
        assert "platforms" in first_game
        assert "genres" in first_game
        assert "categories" in first_game