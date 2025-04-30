# Use a base image with build tools
FROM python:3.10-slim

# Avoid interactive prompts during builds
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    libmariadb-dev \  
    pkg-config \
    curl \
    git \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your project
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the app on port 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
