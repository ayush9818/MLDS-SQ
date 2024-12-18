# Making a connection in Flask

There is added complexity to maintaining a connection within a Flask app. The Python package `flask_sqlalchemy` helps with this and wraps around SQLAlchemy to do so.

It relies on the URI being provided as a Flask configuration, `SQLALCHEMY_DATABASE_URI`, which can be provided in `flaskconfig.py` (see [here](https://github.com/MSIA/2022-msia423-template-repository/blob/main/config/flaskconfig.py) in the example project).

The database is then connected to by instantiating a `flask_sqlalchemy.SQLAlchemy` object with the flask application object, `app` as its input.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_pyfile("config/flaskconfig.py")

# Initialize the database (requires SQLALCHEMY_DATABASE_URI
# in the imported config object)
db = SQLAlchemy(app)

# Get a session
session = db.session

# Create connection
conn = db.engine.connect().connection
```
