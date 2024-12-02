# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to avoid .pyc files and ensure we are not in interactive mode
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (e.g., for PostgreSQL, if needed)
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000

# Set the entry point for running Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
