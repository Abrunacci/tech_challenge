# Tech challenge

FastAPI offline challenge

### System Requirements

* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)

### Run application

```shell
git pull https://github.com/Abrunacci/tech_challenge.git
cd tech_challenge
docker-compose build
docker-compose up
```

### End application

```shell
docker-compose down
```

### Run tests

```shell
docker-compose up -d
docker-compose exec api pytest . -v --cov-report  --cov
docker-compose down
```

# API Test Coverage:

```shell
---------- coverage: platform linux, python 3.10.13-final-0 ----------
Name                                       Stmts   Miss  Cover
--------------------------------------------------------------
src/connectors/elasticsearch.py                5      0   100%
src/connectors/external_api_connector.py      36      0   100%
src/exceptions/get_movie_exception.py          4      0   100%
src/exceptions/seed_movie_exception.py         4      0   100%
src/main.py                                   13      0   100%
src/mappings/movies.py                         1      0   100%
src/routers/movies.py                         22      0   100%
src/services/elasticsearch_movies.py          47      0   100%
src/services/movies.py                        27      0   100%
--------------------------------------------------------------
TOTAL                                        159      0   100%

```

# API Endpoints

### [GET] http://0.0.0.0:8000

    Redirects to API documentation.

    curl 'http://0.0.0.0:8000'

### [PUT] http://0.0.0.0:8000/api/movies/seed

    Populates the elasticsearch index with data received 
    from external API.

    Request from shell:
        curl -X 'PUT' 'http://0.0.0.0:8000/api/movies/seed' -H 'accept: application/json'

    It can be called with two query parameters:

        title: str
    
            Full or partial movie name.

            curl -X 'PUT' 'http://0.0.0.0:8000/api/movies/seed?title=<full_or_partial_title>' -H 'accept: application/json'
    
        page: int
    
            The external API page.
    
            curl -X 'PUT' 'http://0.0.0.0:8000/api/movies/seed?page=<page_number>' -H 'accept: application/json'
        
        Query combination:
    
         - The use of only one query param will seed the index with all the movies matching that parameter.
         - Using both parameters will seed the index with only the movies that fit both search criteria.
         - The lack of parameters will seed all the movies to the index.

           curl -X 'PUT' 'http://0.0.0.0:8000/api/movies/seed?Title=<full_or_partial_title>&page=<page_number>' -H 'accept: application/json'

    Returns: 
        dict ex: {
            "created": 866,
            "failed": [<List of movies that wasn't inserted in the index>]
        }

    Raises:
        In case of an internal error this endpoint will return a dict with the error string representation

### [GET] http://0.0.0.0:8000/api/movies

    This endpoint returns all the movies required by the client.

    It can be called with two query parameters:

        title: str

            Full or partial movie name.

            curl -X 'PUT' 'http://0.0.0.0:8000/api/movies?title=<full_or_partial_title>' -H 'accept: application/json'

        year: int

            The year of the movie release.

            curl -X 'PUT' 'http://0.0.0.0:8000/api/movies?year=<page_number>' -H 'accept: application/json'

    Query combination:

        - The use one of the query params will return all the movies matching that parameter.
        - Using both parameters will return only the movies that fit both search criteria.
        - The lack of parameters will return all the movies in the elasticsearch index.

          curl -X 'PUT' 'http://0.0.0.0:8000/api/movies?Title=<full_or_partial_title>&year=<year>' -H 'accept: application/json'

    Pagination:

        Not implemented

    Raises:
        In case of an internal error this endpoint will return a dict with the error string representation
    
    Returns: 
        [
            {"Title": "Title", "Year": 2023, "imdbID": "someID"},
            {"Title": "Title", "Year": 2023, "imdbID": "someID"},
            {"Title": "Title", "Year": 2023, "imdbID": "someID"},
            {"Title": "Title", "Year": 2023, "imdbID": "someID"},
            {"Title": "Title", "Year": 2023, "imdbID": "someID"},
            {"Title": "Title", "Year": 2023, "imdbID": "someID"},
        ]