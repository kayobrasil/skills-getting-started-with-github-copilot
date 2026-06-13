import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    # Arrange: deep copy original in-memory state
    original = copy.deepcopy(activities)

    # Act: create TestClient
    client = TestClient(app)

    # Provide client to tests
    yield client

    # Teardown: restore original in-memory state
    activities.clear()
    activities.update(original)
