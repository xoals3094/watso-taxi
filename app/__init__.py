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

    from app.api.taxi_group.taxi_api import taxi_router
    api.include_router(taxi_router)

    from app.api.auth.auth import auth_router
    api.include_router(auth_router)

    app.include_router(api)
    return app
