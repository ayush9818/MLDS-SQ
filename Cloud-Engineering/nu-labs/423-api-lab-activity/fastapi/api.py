from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return "Welcome to my app"


@app.get("/hello")
def hello():
    return "Hello World"


@app.get("/hello/{name}")
def hello_friend(name: str):
    return f"Hello {name}"


class GreetingLanguage(Enum):
    ENGLISH = "english"
    SPANISH = "spanish"
    HINDI = "hindi"


GREETINGS = {
    GreetingLanguage.ENGLISH: "Welcome back",
    GreetingLanguage.SPANISH: "Bienvenido de nuevo",
    GreetingLanguage.HINDI: "Aapaka svaagat hai",
}


class Greeting(BaseModel):
    name: str
    language: GreetingLanguage


@app.post("/hello")
def greet(greeting: Greeting):
    return {"Greeting": f"{GREETINGS[greeting.language]}, {greeting.name}"}
