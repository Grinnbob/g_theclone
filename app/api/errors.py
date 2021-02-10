from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import AppErrors

def setup_error_handler(app):
    @app.exception_handler(AppErrors)
    async def unicorn_exception_handler(request: Request, exc: AppErrors):
        return JSONResponse(
            status_code=422,
            content={"message": f"{exc.message}"}
        )
