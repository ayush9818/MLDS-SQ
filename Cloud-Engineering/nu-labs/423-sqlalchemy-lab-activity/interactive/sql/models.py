import logging
import os

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

# Set up sqlite connection
ENGINE_STRING = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:////tmp/tracks.db")
engine = create_engine(ENGINE_STRING)

# Set up logging config
logger = logging.getLogger(__name__)

# Create a db session
Session = sessionmaker(bind=engine)


class Track(Base):
    """Song (track) with artist and album information"""

    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    duration = Column(Integer, index=True, doc="Specifies track duration in seconds")

    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))

    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")

    def __repr__(self):
        return f'<Track: "{self.title}">'


class Album(Base):
    """Album containing songs"""

    id = Column(Integer, primary_key=True)

    __tablename__ = "albums"
    name = Column(String(100))
    year = Column(Integer)

    artist_id = Column(Integer, ForeignKey("artists.id"))

    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Album: {self.name}, {self.year}>"


class Artist(Base):
    """Artist may have many albums"""

    __tablename__ = "artists"
    id = Column(Integer, primary_key=True)

    name = Column(String(100))

    albums = relationship("Album", back_populates="artist", cascade="all, delete-orphan")
    tracks = relationship("Track", back_populates="artist", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Artist: {self.name}>"


if __name__ == "__main__":
    # Create the tracks table
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

    Base.metadata.create_all(engine)
    logger.info("Database created!")
