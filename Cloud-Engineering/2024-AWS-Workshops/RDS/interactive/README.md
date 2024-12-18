# Interactive Activity

## 0. Export Connection Variables

Export your connection details to an active shell session and verify their values.

```shell
source .mysqlconfig
echo $MYSQL_HOST
```

## 1. Connect to Database

Inspect your database from a mysql client using the `mysql` docker image

```shell
docker run -it --rm \
    mysql:8.0.32 \
    mysql \
    -h$MYSQL_HOST \
    -u$MYSQL_USER \
    -p$MYSQL_PASSWORD
```

```mysql
show databases;
use mlds;
show tables;
```

## 2. Build Docker Image

Build the example Docker image to create tables/records in the database.

```shell
docker build -t penny_mysql .
```

## 3. Run Docker Container

This docker container will run [`penny_lane_db.py`](./penny_lane_db.py) which connects to the database via SqlAlchemy (more on this in the SqlAlchemy Lab) and creates tables and adds records.

```shell
docker run -it \
    --env SQLALCHEMY_DATABASE_URI \
    penny_mysql
```

## 4. Verify Changes

Repeat [step 1](#1-inspect-your-database-from-a-mysql-client) to verify changes to the database
