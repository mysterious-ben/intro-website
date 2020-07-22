# Use the Debian image with python
FROM python:3.8.5-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 8001

# run the command to start the server
CMD ["python", "-m", "src.app"]
