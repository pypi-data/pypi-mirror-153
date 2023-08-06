from fastapi import FastAPI

from servicefoundry.service.fastapi.metrics_router import metrics_router
from servicefoundry.service.fastapi.prometheus_middleware import PrometheusMiddleware


def app():
    _app = FastAPI()
    _app.add_middleware(PrometheusMiddleware)
    _app.add_route("/metrics", metrics_router)

    return _app
