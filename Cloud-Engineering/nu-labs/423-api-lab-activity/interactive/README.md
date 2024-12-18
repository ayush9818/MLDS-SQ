# Interactive example

| HTTP method | Description                                           | Example                                   | Request URL/data                                    | Response status code/body |
| ----------- | ----------------------------------------------------- | ----------------------------------------- | --------------------------------------------------- | ------------------------- |
| `GET`       | Asks the server to retrieve a resource.               | Retrieve records by `value1` and `value2` | <https://httpbin.org/get?key1=value1&key2=value2>   | `HTTP/1.1 200 OK`         |
| `POST`      | Asks the server to create a new entry.                | Add an entry                              | <https://httpbin.org/post> data = {'key1':'value1'} | `HTTP/1.1 201 CREATED`    |
| `PUT`       |  Asks the server to edit/update an existing resource. | Update an entry                           | <https://httpbin.org/put> data={"key1":"value1"}    | `HTTP/1.1 200 OK`         |
| `DELETE`    | Asks the server to delete a resource.                 | Delete an entry                           | <https://httpbin.org/delete> data={"key1":"value1"} | `HTTP/1.1 200 OK`         |

```python
import requests
url = "https://httpbin.org"

r = requests.get(f"{url}/get", params={"key1": "value1", "key2": "value2"})
# Equivalent to "https://httpbin.org/get?key1=value1&key2=value2
print(r.status_code, r.json())

r = requests.post(f"{url}/post", data={"string": "yarn", "number": 42})
print(r.status_code, r.json())

r = requests.put(f"{url}/put", data={"string": "rope", "number": 43})
print(r.status_code, r.json())

r = requests.delete(f"{url}/delete", params={"string": "rope"})
print(r.status_code, r.json())
```

## Making API calls

### GET

Makes a GET call, requesting a resource from `https://httpbin.org/get` where the `key1` is `value1`:

#### GET with CURL

`-X` specifies the type of request

```bash
curl -X GET "https://httpbin.org/get?key1=value1"
```

#### GET with python requests

```python
import requests
payload = {"key1": "value1", "key2": "value2"}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.text)
```

### POST

Makes a POST call, adding a new entry to URL.

#### POST with CURL

`curl -i -H "Content-Type: application/json" -X POST -d "{'key1': 'value1', 'key2':'value2'}" https://httpbin.org/post`

- `-H` specifies the header, which tells the API that it is receiving the data in JSON form.
- `-d` specifies the data being posted.
- `-i` denotes to include a header in the output

(you can also use [explainshell](https://explainshell.com) to explain any new bash commands you see! [explain the above command](https://explainshell.com/explain?cmd=curl+-i+-H+%22Content-Type%3A+application%2Fjson%22+-X+POST+-d+%22%7B%27key1%27%3A+%27value1%27%2C+%27key2%27%3A%27value2%27%7D%22+https%3A%2F%2Fhttpbin.org%2Fpost))

To see all `curl` options, run `curl -h` from your command line.

#### POST with python requests

```python
import requests

r = requests.post('https://httpbin.org/post', data = {'key1': 'value1', \
'key2': ['value2', 'value3']})
print(r.text)
```

## Exercise

- Ingest weather data from the OpenWeatherMap API
- Sign up for an OpenWeatherMap [API key](http://openweathermap.org/appid)
- Ingest weather data for the city of your choice using the [current weather API](https://openweathermap.org/current)

  1. Make the request via your browser

     <https://api.openweathermap.org/data/2.5/weather?q=CITY&appid=API_KEY>
     where `CITY` and `API_KEY` need to be filled out.
     For instance, <https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=random_hashed_api_key>

  2. Make the request with `curl` from the command line
  3. Make these requests via [Python Requests library](https://3.python-requests.org/)
  4. Make the same request but get the response back in XML
  5. Make the same request but get the response back in metric units

> Hint: check the [API Documentation for examples](https://openweathermap.org/current)

## Using the Dockerfile

The included Dockerfile can be used to build and run an image with the example python code.

To build the image:

```shell
docker build -t api-lab .
```

To run the example script:

```shell
docker run api-lab example.py
```

To run the openweather script:

```shell
export OPENWEATHER_API_KEY="your-api-key"
docker run --env OPENWEATHER_API_KEY api-lab openweather.py
```

To run an interactive `ipython` session:

```shell
docker run -it --entrypoint ipython api-lab
```
