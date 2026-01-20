# Video Game API
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Flask-based REST API providing access to detailed Steam games data, including genres, categories, platforms, ratings, and tags.  
The API supports secure access with Bearer tokens and allows filtering games by multiple parameters.

## Features
- User authentication & JWT-based Bearer token system  
- Three API endpoints:
  - `/api/games` — search games with multiple filters  
  - `/api/games/by-tag` — search games by SteamSpy tag  
  - `/api/tags` — list all available tags  
- Supports filters by name, genre, category, platform, release year, rating range, and price range  
- JSON responses with structured data and counts  
- Example docs included in the web app
- Minimalistic user-friendly design using Bootstrap

## Dataset

This project uses data sourced from Kaggle (https://www.kaggle.com/datasets/nikdavis/steam-store-games?select=steam.csv), which includes detailed game information and metadata.

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies (requirements.txt).
4. The project uses a `.env` file for configuration. Create a `.env` file in the root directory of the project and add the variable `SECRET_KEY` with the value being a secure string of personal choice.
5. Initialise the auth database (creates `instance/auth.sqlite`):

```bash
python init_db.py
```
6. Start the app:

```bash
python run.py
```
## Docker installation (alternative)

1. Clone the repository.
2. Create a `.env` file in the project root and add `SECRET_KEY` (same as the standard installation).
3. Build and start the container:

```bash
docker compose up --build
```

4. First-time only - initialise the auth database in a second terminal (creates tables in the Docker named volume):

```bash
docker compose run --rm web python init_db.py
```

5. Open the app:

http://127.0.0.1:5000/

6. Stop the container:

```bash
docker compose down
```

## Using the API

All API endpoints require a valid Bearer token in the request headers.

### Authentication

1. Register an account via the web interface.  
2. Log in and generate a token.
3. Once generated the token will expire in 1 hour giving users the option to generate a new one once more.
4. Include the token in your requests:

"Authorization: Bearer `YOUR_TOKEN`" http://127.0.0.1:5000/api/games?name=Half-Life

### Endpoints

There are 2 main and 1 auxiliary endpoints available.

#### `/api/games`

Returns detailed information about Steam games. Requires a name parameter, with optional filters such as genre, platform, category, release year, price range, and rating.

##### Parameters

| Parameter     | Type    | Required | Description |
|---------------|---------|----------|-------------|
| name          | string  | Yes      | Game name or partial name to search for |
| release_year  | string  | No       | Filter by release year (YYYY) |
| genre         | string  | No       | Filter by genre name |
| platform      | string  | No       | Filter by platform name |
| category      | string  | No       | Filter by category name |
| rating_min    | float   | No       | Minimum rating percentage (0–100) |
| rating_max    | float   | No       | Maximum rating percentage (0–100) |
| price_min     | float   | No       | Minimum price in GBP |
| price_max     | float   | No       | Maximum price in GBP |

##### Example request (Python)

```python
import requests

headers = {
    "Authorization": "Bearer <YOUR_TOKEN>"
}

params = {
    "name": "Half-Life",       # required
    "genre": "Action",         # optional
    "platform": "windows",     # optional
    # ...other optional filters available
}

response = requests.get("https://your-api-domain.com/api/games", headers=headers, params=params)
print(response.json())
```
##### Example request (cURL)

```bash
curl -H "Authorization: Bearer <YOUR_TOKEN>" \
"https://your-api-domain.com/api/games?name=Half-Life&genre=Action&platform=windows"
```

##### Example JSON response

```python
{
    "count": 2,
    "results": [
        {
            "appid": 70,
            "name": "Half-Life",
            "release_date": "1998-11-19",
            "developer": "Valve",
            "publisher": "Sierra Studios",
            "price": 8.99,
            "overall_rating": 96.5,
            "header_image": "https://steamcdn-a.akamaihd.net/steam/apps/70/header.jpg?t=1530045175",
            "genres": ["Action", "Sci-fi"],
            "categories": ["Single-player"],
            "platforms": ["windows"]
        },
        {
            "appid": 220,
            "name": "Half-Life 2",
            "release_date": "2004-11-16",
            "developer": "Valve",
            "publisher": "Valve",
            "price": 9.99,
            "overall_rating": 97.2,
            "header_image": "https://steamcdn-a.akamaihd.net/steam/apps/220/header.jpg?t=1541802014",
            "genres": ["Action", "Sci-fi"],
            "categories": ["Single-player"],
            "platforms": ["windows"]
        }
    ]
}
```

#### `/games/by-tag`

##### Parameters

| Parameter    | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| tag         | string | Yes      | Exact SteamSpy tag name                  |
| platform    | string | No       | Filter by platform name                  |
| rating_min  | float  | No       | Minimum rating percentage (0–100)       |
| rating_max  | float  | No       | Maximum rating percentage (0–100)       |
| price_min   | float  | No       | Minimum price in GBP                     |
| price_max   | float  | No       | Maximum price in GBP                     |

##### Example request (Python)


```python
import requests

headers = {
    "Authorization": "Bearer <YOUR_TOKEN>"
}

params = {
    "tag": "Survival",   # required
    "platform": "windows"  # optional
    # ...other optional filters available
}

response = requests.get("https://your-api-domain.com/api/games/by-tag", headers=headers, params=params)
print(response.json())
```

##### Example request (cURL)

```bash
curl -H "Authorization: Bearer <YOUR_TOKEN>" \
"https://your-api-domain.com/api/games/by-tag?tag=Survival&platform=windows"
```

##### Example JSON response

```python
{
    "count": 2,
    "results": [
        {
            "appid": 242760,
            "name": "The Forest",
            "release_date": "2018-04-30",
            "price": 14.99,
            "overall_rating": 86.3,
            "header_image": "https://steamcdn-a.akamaihd.net/steam/apps/242760/header.jpg?t=1527008565",
            "platforms": ["windows"]
        },
        {
            "appid": 815370,
            "name": "Green Hell",
            "release_date": "2019-09-06",
            "price": 19.99,
            "overall_rating": 82.1,
            "header_image": "https://steamcdn-a.akamaihd.net/steam/apps/815370/header.jpg?t=1554151175",
            "platforms": ["windows"]
        }
    ]
}
```

#### `/tags` (auxiliary)

The endpoint has no parameters and lists all available SteamSpy tags that can be passed as the required parameter in the "games/by-tag" endpoint.

##### Example request (Python)

```python
import requests

headers = {
    "Authorization": "Bearer <YOUR_TOKEN>"
}

response = requests.get("https://your-api-domain.com/api/tags", headers=headers)
print(response.json())
```

##### Example request (cURL)

##### Example request (cURL)

```bash
curl -H "Authorization: Bearer <YOUR_TOKEN>" \
"https://your-api-domain.com/api/tags"
```

##### Example JSON response

```json
{
    "count": 10,
    "results": [
        "Action",
        "Adventure",
        "RPG",
        "Shooter",
        "Survival",
        "Strategy",
        "Simulation",
        "Sports",
        "Indie",
        "Casual",
        ...
    ]
}
```

## License
This project is licensed under the MIT License.

## Contributing
Feel free to open issues or submit pull requests.

## Live Demo

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://heronvalev.pythonanywhere.com/)






