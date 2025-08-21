from flask import Blueprint, request, jsonify
from sqlalchemy import select
from . import db
from .models import (
    Game,
    Rating,
    Genre,
    GameGenre,
    SteamSpyTag,
    GameSteamSpyTag,
    Category,
    GameCategory,
    Platform,
    GamePlatform,
    GameMedia
)
import json
from flask import Response

# Create a blueprint for the API routes
api_bp = Blueprint("api", __name__)

# Game Details endpoint: search games with filters
@api_bp.route("/games", methods=["GET"])
def get_games():

    # Fetch query parameters
    name = request.args.get("name")
    release_year = request.args.get("release_year")
    platform = request.args.get("platform")
    genre = request.args.get("genre")
    category = request.args.get("category")
    rating_min = request.args.get("rating_min", type=float)
    rating_max = request.args.get("rating_max", type=float)
    price_min = request.args.get("price_min", type=float)
    price_max = request.args.get("price_max", type=float)

    # Require the 'name' parameter
    if not name:
        return jsonify({"error": "The 'name' parameter is required"}), 400

    # Base query selecting the tables
    stmt = (
        select(Game, Rating, GameMedia)
        .join(Rating, Game.appid == Rating.appid)
        .join(GameMedia, Game.appid == GameMedia.appid)
    )

    # Optional filters
    if name:
        stmt = stmt.where(Game.name.ilike(f"%{name}%"))

    if release_year:
        stmt = stmt.where(Game.release_date.like(f"{release_year}%"))

    if genre:
        stmt = (
            stmt.join(GameGenre, Game.appid == GameGenre.appid)
                .join(Genre, GameGenre.genre_id == Genre.genre_id)
                .where(Genre.genre_name == genre)
        )

    if platform:
        stmt = (
            stmt.join(GamePlatform, Game.appid == GamePlatform.appid)
                .join(Platform, GamePlatform.platform_id == Platform.platform_id)
                .where(Platform.platform_name == platform)
        )

    if category:
        stmt = (
            stmt.join(GameCategory, Game.appid == GameCategory.appid)
                .join(Category, GameCategory.category_id == Category.category_id)
                .where(Category.category_name == category)
        )

    if rating_min is not None:
        stmt = stmt.where(
            ((Rating.positive_ratings / (Rating.positive_ratings + Rating.negative_ratings)) * 100) >= rating_min
        )
    if rating_max is not None:
        stmt = stmt.where(
            ((Rating.positive_ratings / (Rating.positive_ratings + Rating.negative_ratings)) * 100) <= rating_max
        )

    if price_min is not None:
        stmt = stmt.where(Game.price >= price_min)
    if price_max is not None:
        stmt = stmt.where(Game.price <= price_max)

    results = db.session.execute(stmt).all()

    # Prepare the JSON output
    games_list = []

    for game, rating, media in results:

        # Calculate overall rating as a percentage
        if rating.positive_ratings + rating.negative_ratings > 0:
            overall_rating = (rating.positive_ratings / (rating.positive_ratings + rating.negative_ratings))  * 100
        else:
            overall_rating = None

        # Platforms
        platforms = (
            db.session.execute(
                select(Platform.platform_name)
                .join(GamePlatform, Platform.platform_id == GamePlatform.platform_id)
                .where(GamePlatform.appid == game.appid)
            ).scalars().all()
        )

        # Genres
        genres = (
            db.session.execute(
                select(Genre.genre_name)
                .join(GameGenre, Genre.genre_id == GameGenre.genre_id)
                .where(GameGenre.appid == game.appid)
            ).scalars().all()
        )

        # Categories
        categories = (
            db.session.execute(
                select(Category.category_name)
                .join(GameCategory, Category.category_id == GameCategory.category_id)
                .where(GameCategory.appid == game.appid)
            ).scalars().all()
        )

        # Build the basic game dictionary
        game_dict = {
            "appid": game.appid,
            "name": game.name,
            "release_date": game.release_date,
            "developer": game.developer,
            "publisher": game.publisher,
            "price": game.price,
            "overall_rating": round(overall_rating, 2),
            "header_image": media.header_image,
            "genres": genres,
            "categories": categories,
            "platforms": platforms
        }

        games_list.append(game_dict)
    
    return Response(
        json.dumps({
            "count": len(games_list),
            "results": games_list
        }, ensure_ascii=False), 
        mimetype='application/json'
    )

# Games by Tag endpoint: search games with filters based on SteamSpy Tag
@api_bp.route("/games/by-tag", methods=["GET"])
def get_games_by_tag():

    # Fetch query parameters
    tag = request.args.get("tag")
    platform = request.args.get("platform")
    rating_min = request.args.get("rating_min", type=float)
    rating_max = request.args.get("rating_max", type=float)
    price_min = request.args.get("price_min", type=float)
    price_max = request.args.get("price_max", type=float)

    # Require the "tag" parameter
    if not tag:
        return jsonify({"error": "The 'tag' parameter is required."}), 400
    
    # Base query selecting the tables
    stmt = (
        select(Game, Rating, GameMedia)
        .join(Rating, Game.appid == Rating.appid)
        .join(GameMedia, Game.appid == GameMedia.appid)
        .join(GameSteamSpyTag, Game.appid == GameSteamSpyTag.appid)
        .join(SteamSpyTag, GameSteamSpyTag.steamspy_tag_id == SteamSpyTag.tag_id)
        .where(SteamSpyTag.tag_name.ilike(tag))
    )

    # Optional filters
    if platform:
        stmt = (
            stmt.join(GamePlatform, Game.appid == GamePlatform.appid)
                .join(Platform, GamePlatform.platform_id == Platform.platform_id)
                .where(Platform.platform_name == platform)
        )

    if rating_min is not None:
        stmt = stmt.where(
            ((Rating.positive_ratings / (Rating.positive_ratings + Rating.negative_ratings)) * 100) >= rating_min
        )
    if rating_max is not None:
        stmt = stmt.where(
            ((Rating.positive_ratings / (Rating.positive_ratings + Rating.negative_ratings)) * 100) <= rating_max
        )

    if price_min is not None:
        stmt = stmt.where(Game.price >= price_min)
    if price_max is not None:
        stmt = stmt.where(Game.price <= price_max)

    results = db.session.execute(stmt).all()

    # Prepare the JSON output
    games_list = []

    
    for game, rating, media in results:

        # Calculate overall rating as a percentage
        if rating.positive_ratings + rating.negative_ratings > 0:
            overall_rating = (rating.positive_ratings /
                            (rating.positive_ratings + rating.negative_ratings)) * 100
        else:
            overall_rating = None

        # Platforms
        platforms = (
            db.session.execute(
                select(Platform.platform_name)
                .join(GamePlatform, Platform.platform_id == GamePlatform.platform_id)
                .where(GamePlatform.appid == game.appid)
            ).scalars().all()
        )

        # Build game dictionary
        game_dict = {
            "appid": game.appid,
            "name": game.name,
            "release_date": game.release_date,
            "price": game.price,
            "overall_rating": round(overall_rating, 2),
            "header_image": media.header_image,
            "platforms": platforms
        }

        games_list.append(game_dict)

    return Response(
        json.dumps({
            "tag": tag,
            "count": len(games_list),
            "results": games_list
        }, ensure_ascii=False), 
        mimetype='application/json'
    )

# Tags endpoint: list all available SteamSpy tags
@api_bp.route("/tags", methods=["GET"])
def get_tags():
    
    # Query all tags from the database
    tags = db.session.execute(
        select(SteamSpyTag.tag_name).order_by(SteamSpyTag.tag_name)
    ).scalars().all()

    return Response(
        json.dumps({
            "count": len(tags),
            "results": tags
        }, ensure_ascii=False),
        mimetype='application/json'
    )