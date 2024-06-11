# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API script to the working directory
COPY api.py .

# Copy the other scripts to the working directory
COPY firebase_helper.py .
COPY misc_helper.py .

# Expose the port on which the API will run
EXPOSE 8000

# Set the command to run the API script
CMD ["python", "main.py"]