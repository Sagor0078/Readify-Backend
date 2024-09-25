
from fastapi import FastAPI 
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"server is startting.... ") 
    from src.books.models import Book   
    await init_db()
    yield
    print("server is stopping")

version = "v1"
# version_prefix = f"/api/{version}"
app = FastAPI(
    title="Readify-Backend",
    description="A REST API for book review web service",
    version=version,
    lifespan=lifespan # add the lifespan event to our application
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])