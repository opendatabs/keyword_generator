FROM python:3.9-slim-buster 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .  # Copy the rest of code into the container

CMD ["python", "keywords_api.py"]