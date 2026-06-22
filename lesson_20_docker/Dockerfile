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

# ENTRYPOINT fixes the interpreter; CMD sets the default script.
# Override CMD by passing arguments to 'docker run':
#   docker run <image>                → python main.py  (default)
#   docker run <image> ui.py          → python ui.py
#   docker run <image> -c "print(1)"  → python -c "print(1)"
ENTRYPOINT ["python"]
CMD ["main.py"]