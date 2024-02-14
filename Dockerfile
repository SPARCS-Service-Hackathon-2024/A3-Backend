# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements files to the container
COPY requirements/requirements.txt requirements/requirements.txt

# Install any needed packages specified in requirements files
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copy the entire FastAPI project to the container
COPY /src /app
# COPY .env /app

# Expose the port that your FastAPI app will run on
EXPOSE 8080

# Define environment variables if needed
# ENV MY_ENV_VARIABLE=my_value

# Run main.py when the container launches
CMD uvicorn --host=0.0.0.0 --port 8000 main:app