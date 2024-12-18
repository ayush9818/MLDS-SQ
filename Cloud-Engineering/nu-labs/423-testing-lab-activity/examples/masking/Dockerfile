FROM python:3.9-slim-buster

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install pytest==7.0.1

COPY . /app


CMD ["python3", "-m", "pytest"]