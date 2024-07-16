from fastapi import FastAPI, APIRouter
from src.auth_container import AuthContainer
from src.taxi_container import TaxiContainer
from src.payment_container import PaymentContainer

from .exception_handing import domain_exception_handler, query_exception_handler, auth_exception_handler


def create_app():
    AuthContainer()
    TaxiContainer()
    PaymentContainer()

    app = FastAPI()
    domain_exception_handler.domain_exception_handler(app)
    query_exception_handler.query_exception_handler(app)
    auth_exception_handler.auth_exception_handler(app)

    api = APIRouter(prefix='/api')

    from app.api.taxi_group.taxi_api import taxi_router
    api.include_router(taxi_router)

    from app.api.auth.auth import auth_router
    api.include_router(auth_router)

    app.include_router(api)
    return app
