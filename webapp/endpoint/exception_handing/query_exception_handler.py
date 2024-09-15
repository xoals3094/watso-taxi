from webapp.common.exceptions import persistence
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def query_exception_handler(app: FastAPI):
    @app.exception_handler(persistence.ResourceNotFound)
    def resource_not_found_exception(request: Request, exc: persistence.ResourceNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'msg': '리소스를 찾을 수 없습니다'}
        )
