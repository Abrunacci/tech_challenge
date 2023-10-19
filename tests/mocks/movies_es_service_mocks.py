example_movie_list = [
    {
        "Title": "Star Wars: Episode IV - A New Hope",
        "Year": 1977,
        "imdbID": "tt0076759",
    },
    {
        "Title": "Star Wars: Episode V - The Empire Strikes Back",
        "Year": 1980,
        "imdbID": "tt0080684",
    },
    {
        "Title": "Star Wars: Episode VI - Return of the Jedi",
        "Year": 1983,
        "imdbID": "tt0086190",
    },
]


transformed_movie_list = [
    {
        "_op_type": "create",
        "_index": "movies",
        "_type": "document",
        "_id": "tt0076759",
        "doc": {
            "Title": "Star Wars: Episode IV - A New Hope",
            "Year": 1977,
            "imdbID": "tt0076759",
        },
    },
    {
        "_op_type": "create",
        "_index": "movies",
        "_type": "document",
        "_id": "tt0080684",
        "doc": {
            "Title": "Star Wars: Episode V - The Empire Strikes Back",
            "Year": 1980,
            "imdbID": "tt0080684",
        },
    },
    {
        "_op_type": "create",
        "_index": "movies",
        "_type": "document",
        "_id": "tt0086190",
        "doc": {
            "Title": "Star Wars: Episode VI - Return of the Jedi",
            "Year": 1983,
            "imdbID": "tt0086190",
        },
    },
]
