from fastapi import FastAPI

from webapp.endpoint.auth import auth_router
from webapp.endpoint.taxi import taxi_router
from webapp.endpoint.user import user_router
from webapp.common.src.auth_container import AuthContainer
from webapp.common.src.user_container import UserContainer
from webapp.common.src.taxi_container import TaxiContainer

from webapp.endpoint.exception_handing.auth_exception_handler import auth_exception_handler
from webapp.endpoint.exception_handing.domain_exception_handler import domain_exception_handler
from webapp.endpoint.exception_handing.persistance_exception_handler import persistence_exception_handler


def create_app():
    auth_container = AuthContainer()
    user_container = UserContainer()
    taxi_container = TaxiContainer()

    app = FastAPI()
    auth_exception_handler(app)
    domain_exception_handler(app)
    persistence_exception_handler(app)

    app.auth_container = auth_container
    app.taxi_container = taxi_container
    app.user_container = user_container

    app.include_router(auth_router, prefix='/auth', tags=['auth'])
    app.include_router(user_router, prefix='/user', tags=['user'])
    app.include_router(taxi_router, prefix='/taxi', tags=['taxi'])

    return app


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(create_app())
