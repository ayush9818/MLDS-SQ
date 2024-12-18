FROM --platform=linux/x86_64 python:3.9-slim

WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config config
COPY src .

CMD ["python", "main.py"]
