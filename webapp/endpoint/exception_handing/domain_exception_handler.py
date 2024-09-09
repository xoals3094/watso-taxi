from webapp.common.exceptions import domain
from fastapi import Request, status
from fastapi.responses import JSONResponse


def domain_exception_handler(app):
    @app.exception_handler(domain.InvalidState)
    def invalid_status_exception(request: Request, exc: domain.InvalidState):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )

    @app.exception_handler(domain.ParticipationFailed)
    def participation_failed_exception(request: Request, exc: domain.ParticipationFailed):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )

    @app.exception_handler(domain.LeaveFailed)
    def leave_failed_exception(request: Request, exc: domain.LeaveFailed):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )

    @app.exception_handler(domain.VerifyFail)
    def leave_failed_exception(request: Request, exc: domain.VerifyFail):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={'msg': exc.msg}
        )
