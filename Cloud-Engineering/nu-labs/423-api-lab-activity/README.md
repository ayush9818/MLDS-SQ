# APIs

This tutorial walks through the basics of APIs and HTTP Requests and how to make them with `curl` and python `requests`. An activity is also included which involves signing up for an OpenWeather API account and making various requests to fetch data.

## What are APIs?

- APIs are _application programming interfaces_
- They allow products and services to communicate with other products or services without knowing how they are implemented.
  - This can enable faster internal development within a product company as work can be isolated and their interactions defined by APIs.
  - They allow for resources to be opened up to the public and third parties while remaining security and control.
  - They enable companies to leverage external products increase the value of their capabilities.
- They adhere to a set of standards, which makes them simple to use.
- For the context of web APIs, the REST ([Representational State Transfer](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)) standards are often used.

## REST APIs

A _request_ is made by the _client_ to the _server_. The _server_ sends a _response_ to the _client_.

![Request-Response / Client-Server](https://cdn-images-1.medium.com/max/1600/0*bYF8loGdnpHklSKS.gif)

A request consists of:

- A URL (uniform resource locator)
- A method - tells the server what kind of action to take (see section below for types)
- Headers - meta information about the request, including authorization
- Body - the data the client wants to send the server

A response consists of:

- A status code
- Headers - data type of response
- Body - content of response

### Anatomy of a URL

`http://127.0.0.1:8000/items/foo?short=1`

`protocol :// address : port / path/to/resource ? query params`

> query params are separated from path by a `?` and come in `&`-separated `key=value` pairs

### Types of HTTP request methods

#### Mock example

| HTTP method | Description                                           | Example                                                       | Request URL/data                                                                     | Response status code/body                                                                      |
| ----------- | ----------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `GET`       | Asks the server to retrieve a resource.               | Retrieve songs by Britney Spears                              | `http://pennylanerecs.com/songs?artist="Britney Spears"`                             | `HTTP/1.1 200 OK` data={"songs":[{"artist":"Britney Spears", "song":"Radar", album:"Circus"}]} |
| `POST`      | Asks the server to create a new resource.             | Add a song by Emancipator                                     | `http://pennylanerecs.com/songs` data={"artist": "Emancipator", "song":"Ghost Pong"} | `HTTP/1.1 201 CREATED` body={id:"eman5"}                                                       |
| `PUT`       |  Asks the server to edit/update an existing resource. | Update a song with the identifier `eman5` with the album name | `http://pennylanerecs.com/songs/eman5` data={"album":"Baralku"}                      | `HTTP/1.1 200 OK`                                                                              |
| `DELETE`    | Asks the server to delete a resource.                 | Delete a song with the identifier `imag1`                     | `http://pennylanerecs.com/songs/imag1`                                               | `HTTP/1.1 200 OK`                                                                              |

## FastAPI

You can write your own REST API using most any programming language; there are a multitude of frameworks to make this process easier. For a long time, Flask and Django have competed as the dominant frameworks for writing web applications in Python. However, over the past few years, an alternative, FastAPI, has grown more and more popular. Due to its simplicity and ease of development, we will choose it for demonstration in this course.

FastAPI has _excellent_ documentation that is very beginner-friendly. We will walk through a simple example together, but you should refer to the [FastAPI Docs](https://fastapi.tiangolo.com/) for an in-depth walkthrough and reference.

The example and its instructions can be found in the [fastapi directory](./fastapi/) of this repo.

## Resources

- [Python Requests library documentation](https://docs.python-requests.org/)
- [Python Requests Library guide](https://realpython.com/python-requests)
- [Introduction to using APIs in Python](https://www.dataquest.io/blog/python-api-tutorial/)
- [Create your own API via Flask!](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
- [HTTP with curl](https://everything.curl.dev/http)
