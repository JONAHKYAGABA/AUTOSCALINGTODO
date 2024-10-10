# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (default for Django)
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1

# Run database migrations and start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
