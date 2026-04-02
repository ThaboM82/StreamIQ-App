# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for MySQL, audio, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libmysqlclient-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command to run the app
CMD ["python", "src/app.py"]
