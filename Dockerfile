FROM python:3.10.8-slim-bullseye
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN pip3 install -r requirements.txt

# Copy the Django app code into the container
COPY . /app/

