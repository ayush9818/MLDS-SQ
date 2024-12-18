from time import sleep
from src.example import debug, info, warning, error

DELAY = 1

if __name__ == "__main__":
    debug()
    sleep(DELAY)
    info()
    sleep(DELAY)
    warning()
    sleep(DELAY)
    error()
