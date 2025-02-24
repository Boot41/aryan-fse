# Use the official Python image
FROM python:3.9

# Install netcat for database connection checking
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DB_HOST=postgres
ENV DB_PORT=5432

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port for Django
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
