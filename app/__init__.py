from fastapi import FastAPI
from src.post_container import PostContainer
from src.auth_container import AuthContainer
#from src.user_container import UserContainer
#from src.common_container import CommonContainer


def create_app():
    #UserContainer()
    AuthContainer()
    PostContainer()
    #CommonContainer()

    app = FastAPI()

    @app.get('/callback')
    async def test(code: str):
        print('callback')

    from app.api.post import post_router
    app.include_router(post_router)

    from app.auth.auth import auth_router
    app.include_router(auth_router)

    return app
