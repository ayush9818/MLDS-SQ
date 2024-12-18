# FastAPI

The included application demonstrates the most basic concepts in FastAPI including GET and POST requests, Path Parameters, and Body Data. All of these topics are covered in depth in the [FastAPI User Guide](https://fastapi.tiangolo.com/tutorial). See:

- [First Steps](https://fastapi.tiangolo.com/tutorial/first-steps)
- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Request Body](https://fastapi.tiangolo.com/tutorial/body/)

## Running

The sample application can be run directly or via Docker using the included [Dockerfile](./Dockerfile).

### Running Locally

1. Create a python virtual environment and activate it

```shell
python -m venv .venv
source .venv/bin/activate
```

2. Install the python requirements

```shell
pip install -r requirements.txt
```

3. Run the application with `uvicorn`

```shell
uvicorn api:app --reload
```

4. Visit the application in your browser

[localhost:8000](http://localhost:8000)

### Running with Docker

1. Build the docker image

```shell
docker build -t fastapi-demo .
```

2. Run the container

```shell
docker run -p 8000:8000 fastapi-demo
```

3. Visit the application in your browser

[localhost:8000](http://localhost:8000)

## Interacting with the Application

You can now interact with the FastAPI application in a number of ways.

The easiest way to see your application running is to use the Interactive Docs that are built automatically by FastAPI (docs: [Interactive API Docs](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs)).

Visit: [localhost:8000/docs](http://localhost:8000/docs)

From this page you can view the available routes, their expected request schema, and the structure of their response. Additionally, you can form requests in the browser and submit them to see actual application responses.

Alternatively, you can continue to make requests using `curl` or the python `requests` library. Samples below:

### Curl

GET

```shell
curl http://localhost:8000/hello
```

POST

```shell
curl -H "Content-Type: application/json" \
    -X "POST" http://localhost:8000/hello \
    -d '{"name": "Michael", "language": "spanish"}'
```

### Python Requests

```python
import requests

r = requests.get("http://localhost:8000/hello/Michael")
print(r.json())

print("\n" + "=" * 40 + "\n")

d = {
  "name": "Michael",
  "language": "hindi"
}
r = requests.post("http://localhost:8000/hello", json=d)
print(r.json())
```
