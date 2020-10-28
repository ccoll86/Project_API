#______           _              __ _ _      
#|  _  \         | |            / _(_) |     
#| | | |___   ___| | _____ _ __| |_ _| | ___ 
#| | | / _ \ / __| |/ / _ \ '__|  _| | |/ _ \
#| |/ / (_) | (__|   <  __/ |  | | | | |  __/
#|___/ \___/ \___|_|\_\___|_|  |_| |_|_|\___|

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set up a working directory in /app
WORKDIR /app

# Copy your Flask app into the working directory
COPY . /app

# Install any needed Python packages with pip
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]



