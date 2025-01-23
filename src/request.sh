#!/bin/bash

# Base URL of the API
BASE_URL="http://localhost:8000/api/v1"

# Example: Get all books
echo "Getting all books..."
curl -X GET "$BASE_URL/books" -H "accept: application/json"
echo -e "\n"

# Example: Get a specific book by ID
BOOK_ID=1
echo "Getting book with ID $BOOK_ID..."
curl -X GET "$BASE_URL/books/$BOOK_ID" -H "accept: application/json"
echo -e "\n"

# Example: Create a new book
echo "Creating a new book..."
curl -X POST "$BASE_URL/books" -H "accept: application/json" -H "Content-Type: application/json" -d '{
  "title": "New Book",
  "author": "Author Name",
  "description": "Book description",
  "published_year": 2023
}'
echo -e "\n"

# Example: Update a book
echo "Updating book with ID $BOOK_ID..."
curl -X PUT "$BASE_URL/books/$BOOK_ID" -H "accept: application/json" -H "Content-Type: application/json" -d '{
  "title": "Updated Book Title",
  "author": "Updated Author Name",
  "description": "Updated description",
  "published_year": 2024
}'
echo -e "\n"

# Example: Delete a book
echo "Deleting book with ID $BOOK_ID..."
curl -X DELETE "$BASE_URL/books/$BOOK_ID" -H "accept: application/json"
echo -e "\n"