from fastapi import FastAPI, APIRouter
from src.auth_container import AuthContainer
from src.taxi_container import TaxiContainer

from .exception_handing import domain_exception_handler, psersistence_exception_handler


def create_app():
    AuthContainer()
    TaxiContainer()

    app = FastAPI()
    domain_exception_handler.post_exception_handler(app)
    psersistence_exception_handler.persistence_exception_handler(app)

    api = APIRouter(prefix='/api')

    taxi_api = APIRouter(prefix='/taxi')
    from app.api.taxi import post, point
    taxi_api.include_router(post.post_router)
    taxi_api.include_router(point.point_router)

    from app.auth.auth import auth_router
    api.include_router(auth_router)
    api.include_router(taxi_api)

    app.include_router(api)
    return app
