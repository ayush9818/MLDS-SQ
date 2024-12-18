# SQLAlchemy

## Introduction

From [SQLAlchemy's homepage](https://www.sqlalchemy.org/):

> SQL databases behave less like object collections the more size and performance start to matter; object collections behave less like tables and rows the more abstraction starts to matter. SQLAlchemy aims to accommodate both of these principles.
>
> SQLAlchemy considers the database to be a relational algebra engine, not just a collection of tables. Rows can be selected from not only tables but also joins and other select statements; any of these units can be composed into a larger structure. SQLAlchemy's expression language builds on this concept from its core.
>
> SQLAlchemy is most famous for its object-relational mapper (ORM), an optional component that provides the **data mapper pattern**, where classes can be mapped to the database in open ended, multiple ways - allowing the object model and database schema to develop in a cleanly decoupled way from the beginning.

### Note on ORMs

Object Relation Mappers (ORMs) are developed to make connecting to and interacting with a database more manageable and coherent from an application's programming language. They are not at all required, but they do simplify many of the common patterns and queries that would otherwise have to be built out with raw SQL.

A Database's contents do not always map well to objects (and vice versa). Most ORM's allow you to make use of a "fuzzy" mapping where some of the relations (tables/objects) or some of the properties (columns/attributes) are omitted from the model.

This page from [Full Stack Python](https://www.fullstackpython.com/object-relational-mappers-orms.html) has some more info on the benefits and downsides of using an ORM

![ORMs - RDB Tables to Python Classes](https://www.fullstackpython.com/img/visuals/orms-bridge.png)

## Create a connection

### Connection URI

A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used.

For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/20/core/engines.html).

#### Connection URI for local `sqlite` database

For this lab, we will be using the dialect `sqlite` locally with the default driver. No username or password are necessary and the local file location replaces the `host:port`. You will have seen this type of URI in the example project repository.

> Note: You can easily replace this string with a connection URI pointing at your RDS Database. One major advantage of configuring your application this way is the ease in which you can "swap" databases depending on your use case.

```python
SQLALCHEMY_DATABASE_URI = "sqlite:///relative/path/to/database.db"
```

The three `///` denote that it is a relative path to where the code is being run. You can also define the absolute path with four `////`:

```python
SQLALCHEMY_DATABASE_URI = "sqlite:////Users/mfedell/path/to/database.db"
```

#### Connection URI for Postgres database (in RDS)

We have not yet covered RDS, but you can use SQLAlchemy to connect to remote databases (such as those in AWS RDS) just as easily with the `SQLALCHEMY_DATABASE_URI`. The main difference is that you will have to include a username/password in the connection string and you will supply a remote url ("Host") instead of local filepath.

See [connect_to_rds.md](./docs/connect_to_rds.md) in the docs folder for more info.

### Making a connection

```python
import os
import sqlalchemy
# the engine_string format
#engine_string = "{conn_type}://{user}:{password}@{host}:{port}/{database}"
engine_string = os.getenv("SQLALCHEMY_DATABASE_URI")
# print(engine_string)  # Enable this line if you need to debug, but use caution as it prints your password
engine = sqlalchemy.create_engine(engine_string)
print(f"Connecting to: {engine.url}")  # This will print the connection string *without* revealing password
```

The above code relies on the connection information being available as environment variables. See command line tutorial for a review of exporting these.

## Create a table

### Define your data model

First, you want to define the data model for your table.

Things you need to know to create your data model:

- What are the columns?
- What data types should the columns be?
- What is going to be the primary key?
- Can each field have nulls?
- Should the field consist of unique values?

The following code can be found in sqlalchemy.py

The data model is created as a class that inherits from SQLAlchemy's `declarative_base`:

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy

Base = declarative_base()

class Track(Base):
    """Metadata for individual songs in the database"""

    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    album = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return f"<Track {self.title}>"
```

### Create the database

Then a connection is made to the database given by the `engine_string` and the table is created:

```python
engine = sqlalchemy.create_engine(engine_string)  # Create an engine for connections
Base.metadata.create_all(engine)  # Create all entities (tables, etc.) defined on the Base.metadata object
```

## Ingest data

A _session_ is the SQLAlchemy ORM's "handle" on the database.

From [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1):

> Keep in mind, the [`Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.session.Session") is just a workspace for your objects, local to a particular database connection - if you think of an application thread as a guest at a dinner party, the [`Session`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session "sqlalchemy.orm.session.Session") is the guest’s plate and the objects it holds are the food (and the database… the kitchen?)

More documentation on sessions can be found [here](https://docs.sqlalchemy.org/en/20/orm/session_basics.html#id1)

1. Start a _session_
2. Define actions to perform on the database. Actions include _add_, _query_, _query_all_,
3. _Commit_ those actions to actually execute them.
4. Once all actions have been taken, a session should be _close_d.

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
with Session() as session:
    track = Track(artist="Britney Spears", album="Circus", title="Radar")

    session.add(track)
    session.commit()

    logger.info("Database created with song added: \
    Radar by Britney spears from the album, Circus")
```

To add multiple rows, you can _add_all_:

```python
session.add_all([track1, track2, track3])
```

## Query a table

### Querying using SQLAlchemy ORM

See guide [here](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying) for information on querying with SQLAlchemy's ORM.

The query equivalent to

```sql
SELECT
    title
FROM
    tracks
WHERE
    artist = "Britney Spears"
```

using SQLAlchemy is as follows:

```python
from sqlalchemy import select
statement = select(Track.title)
britney_tracks = session.execute(Track.title).where(Track.artist == "Britney Spears")
```

### Querying in Pandas

Pandas has a nice function, `pandas.read_sql()` which takes as an input a SQL query and the engine. It takes care of the opening of a session, executing the query, committing it, and closing the session for you. Unfortunately, its exception handling is poor and does not set you up for proper exception handling in your own scripts while using it. However, it can be useful during model development.

```python
query = "SELECT COLUMN_NAME FROM tracks WHERE artist = 'Britney Spears'"
df = pd.read_sql(query, con=engine)
```

### A note on SQL strings in Python

Keep in mind that `%` is a special character in Python and therefore you must use two, `%%` in any queries fed through Python. For example,

```sql
SELECT
    COLUMN_NAME
FROM
    tracks
WHERE
    artist LIKE "%Britney%"
```

should be given as

```python
"""
SELECT
    COLUMN_NAME
FROM
    tracks
WHERE
    artist LIKE "%%Britney%%"
"""
```

both in `pandas.read_sql()` and when using `%%read_sql`

## Exercises

1. Decide the data model for a table you will use in your project
    > if you have not identified or are not using a structured database table for your project, you may instead design a data model for a university enrollment system. This system should track Students and Classes as well as Enrollments (many-to-many relationship between Students and Classes)
2. Build a local table in sqlite
3. If ready, ingest your data. If data to be stored in RDS is further down the value chain and not ready yet, seed the table with a mock row.

Make sure the connection string is configurable, so you can reuse the script to create the table in the RDS instance you will set up in the RDS tutorial.
