from exceptions import DomainException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def post_exception_handler(app: FastAPI):
    @app.exception_handler(DomainException.InvalidStateException)
    def invalid_status_exception(request: Request, exc: DomainException.InvalidStateException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )

    @app.exception_handler(DomainException.PostModificationFailedException)
    def post_modification_failed_exception(request: Request, exc: DomainException.PostModificationFailedException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )

    @app.exception_handler(DomainException.ParticipationFailedException)
    def participation_failed_exception(request: Request, exc: DomainException.ParticipationFailedException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )

    @app.exception_handler(DomainException.LeaveFailedException)
    def leave_failed_exception(request: Request, exc: DomainException.LeaveFailedException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )
