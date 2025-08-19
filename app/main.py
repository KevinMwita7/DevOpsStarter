from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

REQUEST_COUNT = Counter(
    "fastapi_request_count",
    "Total number of requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_latency_seconds",
    "Request latency",
    ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method: str = request.method
    endpoint: str = request.url.path

    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)

    REQUEST_COUNT.labels(method, endpoint).inc()
    return response

@app.get("/", response_class=PlainTextResponse)
async def root() -> str:
    return "Hello World!"

@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
