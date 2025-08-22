from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# Create SQLAlchemy models from the database
class Game(db.Model):
    __tablename__ = "games"

    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    release_date: Mapped[str] = mapped_column(String)
    developer: Mapped[str] = mapped_column(String)
    publisher: Mapped[str] = mapped_column(String)
    english: Mapped[int] = mapped_column(Integer)
    short_description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)


class Rating(db.Model):
    __tablename__ = "ratings"

    appid: Mapped[int] = mapped_column(primary_key=True)
    positive_ratings: Mapped[int] = mapped_column(Integer)
    negative_ratings: Mapped[int] = mapped_column(Integer)
    average_playtime: Mapped[int] = mapped_column(Integer)
    median_playtime: Mapped[int] = mapped_column(Integer)
    owners: Mapped[str] = mapped_column(String)
    achievements: Mapped[int] = mapped_column(Integer)
    required_age: Mapped[int] = mapped_column(Integer)


class GameMedia(db.Model):
    __tablename__ = "game_media"

    appid: Mapped[int] = mapped_column(primary_key=True)
    header_image: Mapped[str] = mapped_column(String)


class Category(db.Model):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String)


class GameCategory(db.Model):
    __tablename__ = "game_categories"

    appid: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(primary_key=True)


class Genre(db.Model):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    genre_name: Mapped[str] = mapped_column(String)


class GameGenre(db.Model):
    __tablename__ = "game_genres"

    appid: Mapped[int] = mapped_column(primary_key=True)
    genre_id: Mapped[int] = mapped_column(primary_key=True)


class Platform(db.Model):
    __tablename__ = "platforms"

    platform_id: Mapped[int] = mapped_column(primary_key=True)
    platform_name: Mapped[str] = mapped_column(String)


class GamePlatform(db.Model):
    __tablename__ = "game_platforms"

    appid: Mapped[int] = mapped_column(primary_key=True)
    platform_id: Mapped[int] = mapped_column(primary_key=True)


class SteamSpyTag(db.Model):
    __tablename__ = "steamspy_tags"

    tag_id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String)


class GameSteamSpyTag(db.Model):
    __tablename__ = "game_steamspy_tags"

    appid: Mapped[int] = mapped_column(primary_key=True)
    steamspy_tag_id: Mapped[int] = mapped_column(primary_key=True)

# User authentication model
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

    def set_password(self, password: str) -> None:
        """Hashes and sets the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies the password against the hash."""
        return check_password_hash(self.password_hash, password)