import unittest
from fastapi.testclient import TestClient


class TestHealthChekEndpoints(unittest.TestCase):
    def setUp(self):
        from src.main import app

        self.client = TestClient(app)

    def test_healthy(self):
        response = self.client.get("/v1/healthcheck")

        self.assertEqual(response.status_code, 200)
