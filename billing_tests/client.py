from starlette.testclient import TestClient

from billing.app import app

client = TestClient(app)
