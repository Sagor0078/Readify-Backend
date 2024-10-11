

# Use the official Python slim image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Set environment variable for host
ENV HOST 0.0.0.0

# Command to run the FastAPI application
CMD ["fastapi","run","src","--port","8000","--host","0.0.0.0"]