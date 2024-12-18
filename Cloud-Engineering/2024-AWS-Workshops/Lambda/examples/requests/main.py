import requests


def handler(event, context):
    user = event.get("user", "michaelfedell")
    response = requests.get(f"https://api.github.com/users/{user}/repos")
    if response.ok:
        repos = response.json()
        return [r.get("name") for r in repos]
    else:
        return response.text
