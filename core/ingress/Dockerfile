# Use the official Python image as a base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the requirements file into the container
COPY pyproject.toml uv.lock ./

# Install the dependencies using uv
RUN uv sync

# Copy the FastAPI application code into the container
COPY . .

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uv", "run", "core/ingress/src/main.py"]
