# Logging

The material included in this README is pulled from past years' lecture material for extended reference and information.

The lab activity can be found in the included [Activity.md](./Activity.md).

## Key takeaway

Logging helps you understand what your code is doing and how what it's doing changes over time. It helps in identifying bugs, changes in functionality, input data quality, and more.

## Examples

Execute each script in the archive directory (e.g. `python 00_logging_debug.py`) in numerical order while looking at the script's content to understand each additional piece of logging functionality. The reading below provides context on each script.

## Module outline

<!-- toc -->

- [Logging](#logging)
  - [Key takeaway](#key-takeaway)
  - [Examples](#examples)
  - [Module outline](#module-outline)
- [Introduction](#introduction)
  - [What is logging?](#what-is-logging)
  - [Reasons to log](#reasons-to-log)
    - [During development](#during-development)
    - [In production](#in-production)
- [Concepts: What to log](#concepts-what-to-log)
  - [Data characteristics](#data-characteristics)
  - [Performance profiling](#performance-profiling)
  - [Input or output file paths](#input-or-output-file-paths)
  - [Important actions](#important-actions)
- [Overview of logging components](#overview-of-logging-components)
  - [Four common classes for logging](#four-common-classes-for-logging)
  - [Basic configuration](#basic-configuration)
  - [Levels of logging](#levels-of-logging)
- [Demonstration: Using  `logging`](#demonstration-using--logging)
  - [Levels of logging: Debug](#levels-of-logging-debug)
  - [Levels of logging: Info](#levels-of-logging-info)
  - [Levels of logging: Warning](#levels-of-logging-warning)
  - [Formatting log messages](#formatting-log-messages)
    - [LogRecord attributes](#logrecord-attributes)
    - [Example](#example)
  - [Logging with a timestamp](#logging-with-a-timestamp)
  - [Logging variable data](#logging-variable-data)
  - [Defining a logger](#defining-a-logger)
  - [Logger configuration for modules](#logger-configuration-for-modules)
  - [Logging to a log file](#logging-to-a-log-file)
- [Logging in development and production](#logging-in-development-and-production)
  - [Configuring a logger from a file](#configuring-a-logger-from-a-file)
- [Implementation guidelines](#implementation-guidelines)
  - [Implementation guidelines](#implementation-guidelines-1)
- [Resources](#resources)

<!-- tocstop -->

# Introduction

## What is logging?

Logging is the outputting of messages throughout your code. It is a fancier method of doing so than using `print` statements as it allows for the categorization of messages into different categories (`DEBUG`, `INFO`, `WARNING`, `ERROR`, etc) and can join additional metadata to the message such as the time and date, the file that is being run, the line number of the script where the log is being made, and the function the message is written within.

## Reasons to log

### During development

* To understand what your code is doing at different stages
* To aid in debugging
* To help identify when things aren't happening the way you think they should be

### In production

* To identify failures during operations through monitoring
* To identify when there are changes in your code's functionality when in production
* To assess patterns in the code's inputs and/or outputs over time

# Concepts: What to log

## Data characteristics

Consider when you're developing code in a Jupyter Notebook - what kinds of checks do you do to make sure your code did what you think it did to your data?
</br>

Examples:
</br>

* Size of input data and data after each processing step
* Number of missing values at each step of processing
* Summary statistics

## Performance profiling

How computationally expensive is your code? It can be a good idea to time and log steps such as:

* Load data
* Perform a data processing step
* Train a model
* Score a model
* Integration with external systems
  * Databases
  * APIs
  * ...

## Input or output file paths

* Log when files are loaded or saved and state the explicit paths.
* Loading the wrong auxiliary data files without realizing it is a common mistake and logging can help debug.
* Also denotes usually an important marker in the process

## Important actions

Log when strong decisions are made by the code, such as:

* Dropping rows from a dataset
* Defaulting to a keyword argument because it wasn't provided (but generally should be for reproducibility)
* Any except clauses are invoked

# Overview of logging components

## Four common classes for logging

- **Logger**: object that is used in the application code directly to call logging functions.
- **LogRecord**:  automatically created by the Logger that has all the information related to the event being recorded, including the time, the name of the function containing the logging call, the line number the call is made, the level of severity of the event, and more.
- **Handler**: sends the LogRecords to the output destination, like the console or a file
- **Formatter**: formats the output of the LogRecord to the Handler based on a provided format string, which should include which LogRecord attributes are included.

## Basic configuration

[`logging.basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig)

| Format | Description  |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| *filename* | Specifies that a FileHandler be created, using the specified filename, rather than a StreamHandler.  |
| *filemode* | If *filename* is specified, open the file in this [mode](https://docs.python.org/3/library/functions.html#filemodes). Defaults to `'a'`. |
| *format* | Use the specified format string for the handler. |
| *datefmt*  | Use the specified date/time format, as accepted by `[time.strftime()](https://docs.python.org/3/library/time.html#time.strftime)`. |
| *style*  | If *format* is specified, use this style for the format string. One of `'%'`,`'{'` or `'$'` for [printf-style](https://docs.python.org/3/library/stdtypes.html#old-string-formatting), [`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format) or [`string.Template`](https://docs.python.org/3/library/string.html#string.Template) respectively. Defaults to `'%'`. |
| *level*  | Set the root logger level to the specified [level](https://docs.python.org/3/library/logging.html#levels). |
| *stream* | Use the specified stream to initialize the StreamHandler. Note that this argument is incompatible with *filename* - if both are present, a `ValueError` is raised. |
| *handlers* | If specified, this should be an iterable of already created handlers to add to the root logger. Any handlers which don’t already have a formatter set will be assigned the default formatter created in this function. Note that this argument is incompatible with *filename* or *stream* - if both are present, a `ValueError` is raised.  |

## Levels of logging

| Level  | When it’s used |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DEBUG  | Detailed information, typically of interest only when diagnosing problems. |
| INFO | Confirmation that things are working as expected.  |
| WARNING  | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected. |
| ERROR  | Due to a more serious problem, the software has not been able to perform some function.  |
| CRITICAL | A serious error, indicating that the program itself may be unable to continue running. |

From [Python logging documentation](https://docs.python.org/3/howto/logging.html)

# Demonstration: Using  `logging`

See interactive scripts in `2020-msia423` repository [here](https://github.com/MSIA/2020-msia423/tree/master/logging) and execute the files as you go through this component.

## Levels of logging: Debug

*Interactive*: `0_logging_debug.py`

```python
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("Debuggggg")
logging.info("FYI")
logging.warning("Warning!")
```

Resulting log:

```bash
DEBUG:root:Debuggggg
INFO:root:FYI
WARNING:root:Warning!
```

## Levels of logging: Info

*Interactive*: `1_logging_info.py`

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.debug("Debuggggg")
logging.info("FYI")
logging.warning("Warning!")
```

Resulting log:

```bash
INFO:root:FYI
WARNING:root:Warning!

```

## Levels of logging: Warning

*Interactive*: `2_logging_warning.py`

```python
import logging

logging.basicConfig(level=logging.WARNING)

logging.debug("Debuggggg")
logging.info("FYI")
logging.warning("Warning!")
```

Resulting log:

```bash
WARNING:root:Warning!

```

## Formatting log messages

Log messages can be formatted in a wide range of ways and can include a number of built-in `LogRecord` attributes.

### LogRecord attributes

A number of [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes) can be inserted into log messages including:

| Attribute name | Format  | Description |
| -------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| asctime  | %(asctime)s | Human-readable time when the [`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord) was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time). |
| created  | %(created)f | Time when the [LogRecord](https://docs.python.org/3/library/logging.html#logging.LogRecord) was created (as returned by [`time.time()`](https://docs.python.org/3/library/time.html#time.time)).  |
| filename | %(filename)s  | Filename portion of `pathname`. |
| funcName | %(funcName)s  | Name of function containing the logging call. |
| levelname  | %(levelname)s | Text logging level for the message (`'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`). |
| levelno  | %(levelno)s | Numeric logging level for the message (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).  |
| lineno | %(lineno)d  | Source line number where the logging call was issued (if available).  |
| message  | %(message)s | The logged message, computed as `msg % args`. This is set when [`Formatter.format()`](https://docs.python.org/3/library/logging.html#logging.Formatter.format) is invoked.  |
| module | %(module)s  | Module (name portion of `filename`).  |

### Example

*Interactive*: `3_logging_format.py`

```python
import logging

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s',
                    level=logging.DEBUG)

logging.debug("Debuggggg")
logging.info("FYI")
logging.warning("Warning!")
```

Resulting log:

```bash
root         DEBUG    Debuggggg
root         INFO     FYI
root         WARNING  Warning!
```

## Logging with a timestamp

*Interactive*: `4_logging_datetime.py`

```python
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

logging.debug("Debuggggg")
logging.info("FYI")
logging.warning("Warning!")
```

Resulting log:

```bash
04/12/2020 09:44:50 PM root         DEBUG    Debuggggg
04/12/2020 09:44:50 PM root         INFO     FYI
04/12/2020 09:44:50 PM root         WARNING  Warning!

```

## Logging variable data

*Interactive*: `5_logging_variable.py`

```python
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

class_name = 'MSIA423'
description = 'fun!'

logging.warning("%s is so %s", class_name, description)
```

Resulting log:

```bash
04/12/2020 09:45:16 PM root         WARNING  MSIA423 is so fun!
```

## Defining a logger

Logging using `logging.info()`, `logging.warning()`, etc records the logs as being from `root`. Sometimes, we may want our logs to be more explicit (such as in production) as to what application is creating them.
In this case, we can create a `logging` object, often called `logger`. A logger is defined after the logging configuration has been set up as `logger = logging.getLogger("logger-name")`; typically, it uses the name of the module by calling `logging.getLogger(__name__)`

*Interactive*: `6_logging_logger.py`

```python
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

# Will display 'msia423-logging-module' instead of 'root'
logger = logging.getLogger('msia423-demo')

class_name = 'MSIA423'
description = 'fun!'

logging.warning("%s is so %s", class_name, description)
logger.warning("%s is so %s", class_name, description)
```

## Logger configuration for modules

* Modules should only emit messages, never configure how they are handled.
* It is the responsibility of the importing application to configure how logs are handled.
* Module should use a logger named the same as the module itself so the source of the log can be identified.

```python
import logging

logger = logging.getLogger(__name__)
```

*Interactive*: See `07_logging_with_imports.py` and `08_logging_with_imports.py` to see how the execution script configures the logger that applies to `logmodule.py`.

## Logging to a log file

*Interactive*: `09_logging_logger.py`

```python
import logging.config
import logging

logging.basicConfig(filename='msia423.log', level=logging.DEBUG)
logger = logging.getLogger('msia423-demo')

logger.debug("Debuggggg")
logger.info("FYI")
logger.warning("Warning!")
```

The following will be printed to the file `msia423.log`:

```log
DEBUG:msia423-demo:Debuggggg
INFO:msia423-demo:FYI
WARNING:msia423-demo:Warning!

```

# Logging in development and production

During local development, we want to:

* Include `DEBUG` messages to inform our development so we set our level to DEBUG
* Easily read the log messages
* Easily understand the date and time stamp

During production, we want to:

* Only log what is really necessary, so set level a INFO to remove DEBUG messages
* Have our messages be parsable for analysis --> JSON format
* Have our time stamps ready for analysis -->format as year-month-day to enable sorting and include the time zone

By configuring the logger using a file, that file can be easily swapped out between local development and production.

## Configuring a logger from a file

```python
import logging.config
import logging

logging_config = logging_local.conf

logging.config.fileConfig(logging_config)
logger = logging.getLogger('msia423-demo')

logger.debug("Debuggggg")
logger.info("FYI")
logger.warning("Warning!")

```

The configuration file, `logging_local.conf`:

```toml
[loggers]
keys=root

[handlers]
keys=stream_handler

[formatters]
keys=formatter

[logger_root]
level=DEBUG
handlers=stream_handler

[handler_stream_handler]
class=StreamHandler
level=DEBUG
formatter=formatter
args=(sys.stderr,)

[formatter_formatter]
format=%(asctime)s %(name)-12s %(levelname)-8s %(message)s
datefmt=%m/%d/%Y %I:%M:%S %p
```

See more on setting up your configuration file [here](https://docs.python.org/3/howto/logging.html#configuring-logging).

*Interactive*: See `10_logging_local_fileconfig.py` and `11_logging_production_fileconfig.py` use `logging_local.conf` and `logging_prod.conf`.

# Implementation guidelines

## Implementation guidelines

* Use at least three levels of logging in your code
  * Use logging level `DEBUG` for things you only want to log while developing
  * Use logging level `INFO` for things you want to monitor while in production
  * Use logging level `WARNING` for things that would need attention in production
  * Use logging level `ERROR` for when an exception occurs
* Configure your logging from logging configuration files to allow for easy switching between development and production
* Only configure your logger from the executing script.
* In modules, set up your logger as `logger = logging.getLogger(__name__)`
* Don't commit .log files to git, put `.log` in your `.gitignore`
* Include timestamps in your logs

# Resources

* [https://docs.python.org/3/howto/logging.html](https://docs.python.org/3/howto/logging.html)
* [https://realpython.com/python-logging/](https://realpython.com/python-logging/)
* [https://docs.python-guide.org/writing/logging/](https://docs.python-guide.org/writing/logging/)
