
from fastapi import FastAPI 
from src.books.routes import book_router
from contextlib import asynccontextmanager
# from src.db.main import initdb


#the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):    
    # await initdb()
    print("server is starting")
    yield
    print("server is stopping")

version = "v1"

app = FastAPI(
    title="Readify-Backend",
    description="A REST API for book review web service",
    version=version,
    lifespan=lifespan # add the lifespan event to our application
)

app.include_router(
    book_router,
    prefix="/books",
    tags=['books']
)