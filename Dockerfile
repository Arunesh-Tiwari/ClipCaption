FROM python:3.12.3-slim

RUN apt-get update -qq \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN python -m pip install psycopg[binary]
RUN apt-get update && apt-get install -y postgresql-client

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the script into the image and make it executable
COPY do.sh /code/do.sh
RUN chmod +x /code/do.sh

COPY . .