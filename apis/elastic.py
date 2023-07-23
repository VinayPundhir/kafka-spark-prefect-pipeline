import logging
import os

from elasticsearch import Elasticsearch

from config import CERT_PATH, ELASTIC_HOST, ELASTIC_PORT, ELASTIC_SCHEME

logging.basicConfig(level=logging.INFO)


def get_elastic_connection():
    """function returns new  Elasticsearch instance if established a connection"""
    elastic_username = os.environ.get("ELASTIC_USERNAME")
    elastic_password = os.environ.get("ELASTIC_PASSWORD")

    if not elastic_password:
        raise ValueError("ELASTIC_PASSWORD not found in env")
    if not elastic_username:
        raise ValueError("ELASTIC_USERNAME not found in env")

    return Elasticsearch(
        hosts=[f"{ELASTIC_SCHEME}://{ELASTIC_HOST}:{ELASTIC_PORT}"],
        http_auth=(elastic_username, elastic_password),
        verify_certs=True,
        ca_certs=CERT_PATH,
    )


def push_data_to_elastic(data: list, index_name: str, mapping: dict):
    """function pushes data to elastic index"""
    es = get_elastic_connection()
    es.indices.create(index=index_name, body={"mappings": mapping}, ignore=400)
    for doc in data:
        logging.info(f"push index : {index_name} : {doc}")
        es.index(index=index_name, body=doc)
