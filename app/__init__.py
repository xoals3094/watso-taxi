from fastapi import FastAPI, APIRouter
from src.auth_container import AuthContainer
from src.taxi_container import TaxiContainer
from src.payment_container import PaymentContainer
from src.user_container import UserContainer

from .exception_handing import domain_exception_handler, query_exception_handler, auth_exception_handler


def create_app():
    AuthContainer()
    TaxiContainer()
    PaymentContainer()
    UserContainer()

    app = FastAPI()
    domain_exception_handler.domain_exception_handler(app)
    query_exception_handler.query_exception_handler(app)
    auth_exception_handler.auth_exception_handler(app)

    api = APIRouter(prefix='/api')

    from app.api.taxi_group.taxi_api import taxi_router
    api.include_router(taxi_router)

    from app.api.auth.auth import auth_router
    api.include_router(auth_router)

    from app.api.user.user_api import user_router
    api.include_router(user_router)

    app.include_router(api)
    return app
