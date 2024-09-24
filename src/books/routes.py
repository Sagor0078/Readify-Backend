from fastapi import APIRouter, HTTPException, status
from typing import List
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel

book_router = APIRouter()

@book_router.get("/books", response_model=List[Book])
async def get_all_books():
    return books

@book_router.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: Book) -> Book:
    new_book = book_data.model_dump()  # Assuming model_dump is a method in your schema
    books.append(new_book)
    return new_book

@book_router.get("/book/{book_id}", response_model=Book)
async def get_book(book_id: int) -> Book:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/book/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> Book:
    for book in books:
        if book['id'] == book_id:
            book.update(book_update_data.dict(exclude_unset=True))  # Update only fields that were provided
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return  # No content to return for DELETE
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
