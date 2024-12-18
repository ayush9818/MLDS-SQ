> NOTE: this is included for archive, but we no longer use the "template repository"

# Connect to RDS

The URI for connecting to a PostgreSQL database will take the form:

```python
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@host:port"
```

You will need to install the Python package `psycopg2` (preferably through `pip` for this connection).

If you did not create a virtual environment when trying out our 2022-msia423-template-repository, please do the following step.

```bash
cd path/to/2022-msia423-template-repository
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

We will test our SqlAlchemy setup by connecting to the RDS Instance that we set up in last week's aws-rds tutorial. Make sure that you still have either a `~/.pgpass` file with the credential string, or a `.env` file in the project directory (ignored from git).

```bash
cat << EOF > .env
export PGUSER="YOUR_USERNAME"
export PGPASS="YOUR_PASSWORD"
export PGHOST="localhost"
export PGPORT="5432"
export PGDATABASE="YOUR_DATABASE_NAME"
EOF

# Or...
cat << EOF >> ~/.pgpass
hostname:port:database:username:password
```

> A Note on `.pgpass`: This file allows you to store credentials in a central place that `psql` can reference when you attempt to initiate a connection. It will try to find the appropriate entry in `.pgpass` by matching the specified host to the `hostname` field in `.pgpass`.

```bash
source .env
```

```bash
export SQLALCHEMY_DATABASE_URI="postgresql://${PGUSER}:${PGPASS}@${PGHOST}:${PGPORT}/${PGDATABASE}"
```
