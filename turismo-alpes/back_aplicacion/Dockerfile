# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('stopwords')"

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "pruebaFastAPI:app", "--host", "0.0.0.0", "--reload"]