from os import environ

index_name = environ.get("ELASTICSEARCH_INDEX_NAME", "test_index")

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
    {
        "Title": "Star Wars: Episode VIII - The Last Jedi",
        "Year": 2017,
        "imdbID": "tt2527336",
    },
]

transformed_movie_list = [
    {
        "_op_type": "create",
        "_index": index_name,
        "_id": "tt0076759",
        "_source": {
            "Title": "Star Wars: Episode IV - A New Hope",
            "Year": 1977,
            "imdbID": "tt0076759",
        },
    },
    {
        "_op_type": "create",
        "_index": index_name,
        "_id": "tt0080684",
        "_source": {
            "Title": "Star Wars: Episode V - The Empire Strikes Back",
            "Year": 1980,
            "imdbID": "tt0080684",
        },
    },
    {
        "_op_type": "create",
        "_index": index_name,
        "_id": "tt0086190",
        "_source": {
            "Title": "Star Wars: Episode VI - Return of the Jedi",
            "Year": 1983,
            "imdbID": "tt0086190",
        },
    },
    {
        "_op_type": "create",
        "_index": index_name,
        "_id": "tt2527336",
        "_source": {
            "Title": "Star Wars: Episode VIII - The Last Jedi",
            "Year": 2017,
            "imdbID": "tt2527336",
        },
    },
]
