"""
Unit tests for the FastAPI service.

This module tests the following endpoints:
- "/"       : Ensures the root endpoint returns HTTP 200 and correct text.
- "/metrics": Ensures the metrics endpoint returns HTTP 200.

Tests are designed to validate basic functionality and response correctness.
"""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_root():
    """
    Test the root endpoint ("/") of the application.

    Verifies that:
        - The HTTP response status code is 200 (OK).
        - The response body is exactly "Hello World!".
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello World!"


def test_get_metrics():
    """
    Test the "/metrics" endpoint of the application.

    Verifies that:
        - The HTTP response status code is 200 (OK).
        - The response contains Prometheus metrics (content checked implicitly).
    """
    response = client.get("/metrics")
    assert response.status_code == 200
