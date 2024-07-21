# Use a Python slim base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install curl and other network tools
RUN apt-get update && apt-get install -y curl iputils-ping

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port 5001 for the Flask app
EXPOSE 5001

# Environment variables
ENV OPENAI_API_URL=http://host.docker.internal:8080/v1
ENV OPENAI_API_KEY=sk-no-key-required

# Command to run the Flask app
CMD ["python", "app.py"]