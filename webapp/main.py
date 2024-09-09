from fastapi import FastAPI

from webapp.endpoint.auth import auth_router
from webapp.endpoint.taxi import taxi_router
from webapp.common.src.auth_container import AuthContainer
from webapp.common.src.taxi_container import TaxiContainer


def create_app():
    auth_container = AuthContainer()
    taxi_container = TaxiContainer()

    app = FastAPI()
    app.auth_container = auth_container
    app.taxi_container = taxi_container

    app.include_router(auth_router, prefix='/auth', tags=['auth'])
    app.include_router(taxi_router, prefix='/taxi', tags=['taxi'])

    return app


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(create_app())
