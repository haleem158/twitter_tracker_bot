# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (use actual .env on deployment platform)
ENV PYTHONUNBUFFERED=1

# Run your main script
CMD ["python", "main.py"]