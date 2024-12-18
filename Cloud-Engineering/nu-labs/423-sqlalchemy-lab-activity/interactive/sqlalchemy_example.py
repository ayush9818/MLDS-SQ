import logging

import pandas as pd
from sqlalchemy import select

from sql.models import Album, Artist, Session, Track, engine

session = Session()

# Set up logging config
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if __name__ == "__main__":
    # Add a `record/track
    britney = Artist(name="Britney Spears")
    radar = Track(title="Radar", duration=229, artist=britney)
    circus = Track(title="Circus", duration=192, artist=britney)
    Circus = Album(name="Circus", year=2008, tracks=[radar, circus])

    session.add_all([radar, circus, Circus, britney])
    session.commit()
    logger.info(
        "Added songs by by Britney spears from the album, Circus"
    )

    # To add multiple rows
    # session.add_all([track1, track2])
    taylor = Artist(name="Taylor Swift")
    taylor.albums = [
        Album(name="Red", year=2012, tracks=[
            Track(title="Red", duration=223, artist=taylor),
            Track(title="Starlight", duration=220, artist=taylor),
        ])
    ]
    session.add(taylor)

    # Commit all of the staged changes to the database (execute transaction)
    session.commit()
    logger.info("Added song: Red by Taylor Swift from the album, Red")

    # Query records using sqlalchemy orm query style
    statement = select(Track).join(Artist).filter(Artist.name == "Britney Spears")
    britney_tracks = (
        session.scalars(statement).all()
    )
    print(britney_tracks)

    statement = select(Artist).filter_by(name="Taylor Swift")
    taylor = session.scalar(statement)
    print(taylor)
    print(taylor.tracks)

    # Query records using raw sql
    query = """
    SELECT * FROM tracks
    JOIN artists ON tracks.artist_id = artists.id
    WHERE artists.name LIKE '%%Britney%%'
    """
    df = pd.read_sql(query, con=engine)
    print(df)

    session.close()
