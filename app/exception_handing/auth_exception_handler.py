from exceptions import auth
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def auth_exception_handler(app: FastAPI):
    @app.exception_handler(auth.AccessDenied)
    def access_denied_exception(request: Request, exc: auth.AccessDenied):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'msg': exc.msg}
        )

    @app.exception_handler(auth.TokenExpired)
    def token_expired_exception(request: Request, exc: auth.TokenExpired):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'msg': exc.msg}
        )

    @app.exception_handler(auth.LoginFail)
    def login_fail_exception(request: Request, exc: auth.LoginFail):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'msg': exc.msg}
        )