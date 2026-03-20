import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB_PATH = Path("/tmp/test_cognitive_deception.db")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["USE_LLM"] = "false"
os.environ["ENABLE_KAFKA"] = "false"
os.environ["ENABLE_ELASTIC"] = "false"
os.environ["ENABLE_NEO4J"] = "false"
os.environ["ENABLE_REDIS"] = "false"

from cognitive_deception.api.main import app  # noqa: E402
from cognitive_deception.models.db import Base, get_db  # noqa: E402
from cognitive_deception.models.entities import AttackEvent, AttackSession, ThreatReport  # noqa: F401,E402

TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_db():
    db = TestingSessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
