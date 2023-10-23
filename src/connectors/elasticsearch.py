from os import environ

from elasticsearch import Elasticsearch

elastic_url = (
    f"http://{environ.get('ELASTICSEARCH_HOST')}:{environ.get('ELASTICSEARCH_PORT')}"
)

es = Elasticsearch(elastic_url, verify_certs=False)
