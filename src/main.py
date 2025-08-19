"""
Main application module for a FastAPI service with Prometheus metrics.

This module defines:
- The FastAPI application instance.
- Middleware to capture request metrics (latency and count) for Prometheus.
- Endpoints:
    - "/"       : Root endpoint returning a simple greeting.
    - "/metrics": Exposes Prometheus metrics for monitoring.
"""

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total number of requests", ["method", "endpoint"])

REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["method", "endpoint"])


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """
    Middleware to record Prometheus metrics for each HTTP request.

    Measures:
        - Request latency using REQUEST_LATENCY histogram.
        - Total request count using REQUEST_COUNT counter.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next request handler in the middleware chain.

    Returns:
        Response: The response returned by the next handler.
    """
    method: str = request.method
    endpoint: str = request.url.path

    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)

    REQUEST_COUNT.labels(method, endpoint).inc()
    return response


@app.get("/", response_class=PlainTextResponse)
async def root() -> str:
    """
    Root endpoint returning a simple greeting.

    Returns:
        str: The string "Hello World!" as plain text.
    """
    return "Hello World!"


@app.get("/metrics")
def metrics() -> Response:
    """
    Endpoint exposing Prometheus metrics.

    Returns:
        Response: A plain text response containing the latest Prometheus metrics,
                  with the appropriate Prometheus content type.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
