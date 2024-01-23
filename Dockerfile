# Start with a base image that has Python installed. Lightweight python distribution with minimum dependencies
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose port 5000 of the container for the Flask application to run on
EXPOSE 5000

# Set the command to start the Flask application
CMD ["python", "app.py"]
