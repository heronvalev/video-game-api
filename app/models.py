from . import db

# Create SQLAlchemy models from the database
class Game(db.Model):
    __tablename__ = "games"

    appid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String)
    developer = db.Column(db.String)
    publisher = db.Column(db.String)
    english = db.Column(db.Integer)
    short_description = db.Column(db.Text)
    price = db.Column(db.Float)

class Rating(db.Model):
    __tablename__ = "ratings"

    appid = db.Column(db.Integer, primary_key=True)
    positive_ratings = db.Column(db.Integer)
    negative_ratings = db.Column(db.Integer)
    average_playtime = db.Column(db.Integer)
    median_playtime = db.Column(db.Integer)
    owners = db.Column(db.Text)
    achievements = db.Column(db.Integer)
    required_age = db.Column(db.Integer)

class GameMedia(db.Model):
    __tablename__ = "game_media"

    appid = db.Column(db.Integer, primary_key=True)
    header_image = db.Column(db.Text)

class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.Text)

class GameCategory(db.Model):
    __tablename__ = "game_categories"

    appid = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, primary_key=True)

class Genre(db.Model):
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.Text)

class GameGenre(db.Model):
    __tablename__ = "game_genres"

    appid = db.Column(db.Integer, primary_key=True)
    genre_id = db.Column(db.Integer, primary_key=True)

class Platform(db.Model):
    __tablename__ = "platforms"

    platform_id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.Text)

class GamePlatform(db.Model):
    __tablename__ = "game_platforms"

    appid = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, primary_key=True)

class SteamSpyTag(db.Model):
    __tablename__ = "steamspy_tags"

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text)

class GameSteamSpyTag(db.Model):
    __tablename__ = "game_steamspy_tags"

    appid = db.Column(db.Integer, primary_key=True)
    steamspy_tag_id = db.Column(db.Integer, primary_key=True)