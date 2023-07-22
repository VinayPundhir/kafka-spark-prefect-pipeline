from elasticsearch import Elasticsearch
import ssl
from config import USR_LOGIN,USR_PASS,ELASTIC_HOST_AND_PORT,CERT_PATH
import logging

logging.basicConfig(level=logging.INFO)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


es = Elasticsearch(
    hosts=[
            ELASTIC_HOST_AND_PORT
    ],
    http_auth=(USR_LOGIN, USR_PASS),
    verify_certs=True,
    ca_certs=CERT_PATH,
)


def push_data_to_elastic(data:list, index_name:str, mapping:dict):
    es.indices.create(index=index_name, body={"mappings": mapping}, ignore=400)
    for doc in data:
        logging.info(f'push index : {index_name} : {doc}')
        es.index(index=index_name, body=doc)
