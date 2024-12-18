# Interactive Activity

## 0: Virtual Environment

Create a virtual environment from the included `requirements.txt` and activate it

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optionally, install an `ipykernel` based on the environment for use in jupyter notebooks

```shell
python -m ipykernel install --user --name pennylane --display-name "Python (pennylane)"
```

## 1. SqlAlchemy Example

Run the included `sqlalchemy_example.py` which connects to a local sqlite database (`/tmp/sqlite.db`) with SqlAlchemy (if it does not already exist, "connecting" will create a new .db file). Once connected, it will create the needed tables based on teh `Track` class defined in the script. Lastly, "tracks" are inserted to the database and then queried both with a `sqlalchemy` ORM query, and a `pandas` `read_sql` query.

```shell
python sqlalchemy_example.py
```

## 2. Inspect from Jupyter with Pandas

Run the included `sqlalchemy_notebook_example.py` to inspect the state of the database. This notebook shows how to create a `sqlalchemy` `engine` object and make use of it with Pandas.

## 3. Connect directly with sqlite3

If you would like to connect directly to the same database from a CLI without involving python at all, you can use the `sqlite3` command which should come installed by default on your machine.

```shell
sqlite3 /path/to/sqlite.db
```

Once connected, you can list tables with `.tables`, databases with `.databases`, and help with `.help`. Once you are done, you can disconnect with `.quit`. For more commands, see the [sqlite3 docs](https://sqlite.org/cli.html).

## Changing the Database URI

One of the advantages of `sqlalchemy` is the ability to connect to different databases with minimal configuration changes. You can simply set a new `SQLALCHEMY_DATABASE_URI` environment variable and run the same scripts. If you would like to test this out against a locally running PostgreSQL database, you can easily start a postgres container with Docker and connect to it with your local python scripts via the following:

```shell
export PGPASS="hunter7"
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=$PGPASS -d postgres
export SQLALCHEMY_DATABASE_URI="postgresql://postgres:$PGPASS@localhost:5432"
python sqlalchemy_example.py
```

You can also inspect the database manually by using the `psql` shell. If your database is running in a docker container, this can be done via the following:

```shell
docker exec -it postgres psql -U postgres
```

```sql
\l
\d
SELECT * FROM Tracks;
```

For more information about this image, see the [official DockerHub image](https://hub.docker.com/_/postgres)
