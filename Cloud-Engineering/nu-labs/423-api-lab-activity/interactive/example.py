import requests


if __name__ == "__main__":
    url = "https://httpbin.org"

    r = requests.get(f"{url}/get", params={"key1": "value1", "key2": "value2"})
    # Equivalent to "https://httpbin.org/get?key1=value1&key2=value2
    print(r.status_code, r.text)

    r = requests.post(f"{url}/post", data={"string": "yarn", "number": 42})
    print(r.status_code, r.text)

    r = requests.put(f"{url}/put", data={"string": "rope", "number": 43})
    print(r.status_code, r.text)

    r = requests.delete(f"{url}/delete", params={"string": "rope"})
    print(r.status_code, r.text)
