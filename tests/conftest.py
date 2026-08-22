import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    # Setup: Create a test client
    with TestClient(app) as c:
        yield c
    # Teardown: Code here runs after all tests in the module finish
