# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (needed for compiling some python extensions if necessary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Start script: Run migrations, collect static files, and launch Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --no-input && gunicorn patna_college.wsgi:application --bind 0.0.0.0:8000"]
