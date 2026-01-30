from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

HTTP_REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status_code']
)

HTTP_REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP Request Latency',
    ['method', 'endpoint', 'status_code'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)


ANTIFRAUD_REQUEST_COUNT = Counter(
    'antifraud_requests_total',
    'Total antifraud requests',
    ['result']
)


ANTIFRAUD_PROCESSING_TIME = Histogram(
    'antifraud_processing_seconds',
    'Antifraud processing time',
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)



class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            response = await call_next(request)
            latency = time.time() - start_time

            endpoint = request.url.path


            if endpoint != "/metrics":
                HTTP_REQUEST_COUNT.labels(
                    method=request.method,
                    endpoint=endpoint,
                    status_code=response.status_code
                ).inc()

                HTTP_REQUEST_DURATION.labels(
                    method=request.method,
                    endpoint=endpoint,
                    status_code=response.status_code
                ).observe(latency)

            return response

        except Exception as e:

            latency = time.time() - start_time
            endpoint = request.url.path

            HTTP_REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status_code=500
            ).inc()

            HTTP_REQUEST_DURATION.labels(
                method=request.method,
                endpoint=endpoint,
                status_code=500
            ).observe(latency)

            raise


def get_metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )