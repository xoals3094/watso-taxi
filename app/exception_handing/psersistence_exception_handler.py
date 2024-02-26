from exceptions import PersistenceException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def persistence_exception_handler(app: FastAPI):
    @app.exception_handler(PersistenceException.ResourceNotFoundException)
    def resource_not_found_exception(request: Request, exc: PersistenceException.ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'msg': exc.msg}
        )
