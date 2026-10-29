# main.py

import logging
import uvicorn

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator

from app.operations import add, subtract, multiply, divide


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Initialize FastAPI application
app = FastAPI()


# Configure HTML templates
templates = Jinja2Templates(directory="templates")


# Request model
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


# Successful response model
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")


# Error response model
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


# Handle HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    logger.error(
        f"HTTPException on {request.url.path}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


# Handle validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    error_messages = "; ".join(
        [
            f"{err['loc'][-1]}: {err['msg']}"
            for err in exc.errors()
        ]
    )

    logger.error(
        f"ValidationError on {request.url.path}: {error_messages}"
    )

    return JSONResponse(
        status_code=400,
        content={"error": error_messages}
    )


# Homepage
@app.get("/")
async def read_root(request: Request):

    logger.info("Homepage accessed")

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Addition
@app.post(
    "/add",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def add_route(operation: OperationRequest):

    try:
        result = add(operation.a, operation.b)

        logger.info(
            f"Addition: {operation.a} + {operation.b} = {result}"
        )

        return OperationResponse(result=result)

    except Exception as e:

        logger.error(f"Add Operation Error: {str(e)}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# Subtraction
@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def subtract_route(operation: OperationRequest):

    try:
        result = subtract(operation.a, operation.b)

        logger.info(
            f"Subtraction: {operation.a} - {operation.b} = {result}"
        )

        return OperationResponse(result=result)

    except Exception as e:

        logger.error(f"Subtract Operation Error: {str(e)}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# Multiplication
@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def multiply_route(operation: OperationRequest):

    try:
        result = multiply(operation.a, operation.b)

        logger.info(
            f"Multiplication: {operation.a} * {operation.b} = {result}"
        )

        return OperationResponse(result=result)

    except Exception as e:

        logger.error(f"Multiply Operation Error: {str(e)}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# Division
@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def divide_route(operation: OperationRequest):

    try:
        result = divide(operation.a, operation.b)

        logger.info(
            f"Division: {operation.a} / {operation.b} = {result}"
        )

        return OperationResponse(result=result)

    except ValueError as e:

        logger.error(f"Divide Operation Error: {str(e)}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        logger.error(f"Divide Operation Internal Error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


# Run FastAPI application
if __name__ == "__main__":

    logger.info("Starting FastAPI Calculator Application")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )