from webapp.common.exceptions import query
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def query_exception_handler(app: FastAPI):
    @app.exception_handler(query.ResourceNotFound)
    def resource_not_found_exception(request: Request, exc: query.ResourceNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'msg': exc.msg}
        )
