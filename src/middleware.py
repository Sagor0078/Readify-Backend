from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

# Set up logging
logger = logging.getLogger("uvicorn.access")
logger.disabled = True  # Disable default access logging


def register_middleware(app: FastAPI):
    # Custom logging middleware to log request and response details
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()  # Record the start time of the request

        # Process the request and get the response
        response = await call_next(request)

        # Calculate the time taken to process the request
        processing_time = time.time() - start_time

        # Create a log message with request details and processing time
        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time:.4f}s"

        # Print the log message to the console
        print(message)

        return response

    # CORS middleware to allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        allow_credentials=True,  # Allow credentials (cookies, authorization headers, etc.)
    )

    # Middleware to restrict the allowed hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ],  # Specify the trusted hosts
    )
