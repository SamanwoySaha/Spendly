import pytest
import database.db as db_module
from app import app as flask_app


@pytest.fixture()
def app(tmp_path, monkeypatch):
    test_db = tmp_path / "test_spendly.db"
    monkeypatch.setattr(db_module, "DB_PATH", str(test_db))
    flask_app.config.update({"TESTING": True, "SECRET_KEY": "test-secret"})
    with flask_app.app_context():
        db_module.init_db()
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def registered_user(app):
    from database.db import create_user
    user_id = create_user("Test User", "test@example.com", "password123")
    return {
        "id": user_id,
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    }
