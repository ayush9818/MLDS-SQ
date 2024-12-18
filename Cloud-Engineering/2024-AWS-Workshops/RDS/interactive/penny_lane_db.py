"""Creates and ingests data into a table of songs for the PennyLane."""
import os
import logging

from sqlalchemy import select, text, create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

engine_string = os.getenv("SQLALCHEMY_DATABASE_URI")
if engine_string is None:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI environment variable not set; exiting")
# engine_string = "mysql+pymysql://user:password@host:3306/mlds423_db"

# set up looging config
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__file__)

Base = declarative_base()


class Tracks(Base):
    """Creates a data model for the database to be set up for capturing songs."""

    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    artist = Column(String(100), unique=False, nullable=False)
    album = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return f"<Track {self.title}>"


if __name__ == "__main__":
    # set up mysql connection
    engine = create_engine(engine_string)

    # test database connection
    try:
        engine.connect()
    except OperationalError as e:
        logger.error("Could not connect to database!")
        logger.debug(
            "Database URI: %s",
        )
        raise e

    # create the tracks table
    Base.metadata.create_all(engine)
    logger.info("Database created with Tracks table")

    # create a db session
    Session = sessionmaker(bind=engine)
    session = Session()

    # add a record/track
    radar = Tracks(artist="Britney Spears", album="Circus", title="Radar")
    session.add(radar)
    session.commit()

    logger.info("Added song: Radar by Britney spears from the album, Circus")
    red = Tracks(artist="Taylor Swift", album="Red", title="Red")
    session.add(red)

    # To add multiple rows
    # session.add_all([radar, red])

    session.commit()
    logger.info("Added song: Red by Taylor Swift from the album, Red")

    # query records
    statement = select(Tracks).filter_by(artist="Britney Spears")
    result = session.scalar(statement)
    print(statement)
    print(result)

    query = text("SELECT * FROM tracks WHERE artist LIKE '%%Britney%%'")
    result = session.execute(query).first()
    print(result)

    session.close()
