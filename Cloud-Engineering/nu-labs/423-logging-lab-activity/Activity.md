# Logging Activity

Included is a simple logging example demonstrating some of the helpful log record attributes and how to make use of loggers with config files.

## Activity

Your goal is to set up a logging configuration file to produce the logs according to the following:

- Logs of level `INFO` and higher captured to stdout
  - These should use a "brief" format with just time (second precision), level and log message (feel free to choose one additional attribute)
- Logs of all levels captured to a file
  - These should use a "verbose" format with time (millisecond precision), logger, filename and line number, level and log message

These may look like the following:

stdout

```text
2021-04-13 23:22:45 INFO     this is an info message
2021-04-13 23:22:46 WARNING  this is a warning message
2021-04-13 23:22:46 ERROR    this is an error message
```

file

```text
2021-04-13 23:22:45,435 example  | app.py:10 DEBUG    this is a debug message
2021-04-13 23:22:45,935 example  | app.py:14 INFO     this is an info message
2021-04-13 23:22:46,436 example  | app.py:18 WARNING  this is a warning message
2021-04-13 23:22:46,937 example  | app.py:22 ERROR    this is an error message
```

You may make your modifications to the `root` logger or to the `example` logger used in `example.py`.

You will also need to modify `app.py` to utilize your config file.

## Resources

You can refer to [the course materials](https://github.com/MSIA/2021-msia423/tree/main/logging) or to the python logging documentation:

[Python Logging: Config File Format](https://docs.python.org/3/library/logging.config.html#logging-config-fileformat)

[Python Logging: Log Record Attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)

The [Python Logging "Cookbook"](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook) is also helpful
