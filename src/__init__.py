from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from redis.asyncio import Redis  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"server is startting.... ")
    from src.db.models import Book

    await init_db()
    yield
    print("server is stopping")


version = "v1"
# version_prefix = f"/api/{version}"
app = FastAPI(
    title="Readify-Backend",
    description="A REST API for book review web service",
    version=version,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/review", tags=["reviews"])
