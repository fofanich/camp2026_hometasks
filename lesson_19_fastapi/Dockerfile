FROM python:3.12-slim

# install opencv dependencies for linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* 
# clear cache to save space

WORKDIR /app

COPY ./requirements.txt ./
# install python libraries
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 7860