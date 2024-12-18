import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Decorator for logging
def log_function_call(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Decorator for timing
def time_function_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Example function to be decorated
@log_function_call
@time_function_execution
def example_function(n):
    # Simulate some work
    time.sleep(1)
    return n * n

# Test the decorated function
result = example_function(5)
logging.info(f"Result: {result}")
