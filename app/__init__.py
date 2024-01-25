from fastapi import FastAPI
from src.post_container import PostContainer
from src.auth_container import AuthContainer


def create_app():
    AuthContainer()
    PostContainer()

    app = FastAPI()

    from app.api.post import post_router
    app.include_router(post_router)

    from app.auth.auth import auth_router
    app.include_router(auth_router)

    return app
