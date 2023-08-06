""" services.py (meilisearch, ElasticSearch, Redis, Postgres) """
import logging
import requests
import os


log = logging.getLogger(__name__)

###########
# secrets
SPACES_ACCESS_KEY = os.getenv('SPACES_ACCESS_KEY')
SPACES_SECRET_KEY = os.getenv('SPACES_SECRET_KEY')

ES_HOST = os.getenv('ES_HOST')
ES_PORT = os.getenv('ES_PORT', 9200)
ES_USER = os.getenv('ES_USER', os.getenv('KIBANA_USER', 'kibadmin'))
ES_PASS = os.getenv('ES_PASS', os.getenv('KIBANA_PASS', 'YoUrPaSsWoRd'))
ES_INDEX = os.getenv('ES_INDEX', 'wikipedia')

# secrets
############


def check_es_url(es_host=ES_HOST, es_port=ES_PORT, es_user=ES_USER, es_pass=ES_PASS, es_index=ES_INDEX, es_url=None):
    es_url = es_url or f'http://{ES_USER}:{ES_PASS}@{ES_HOST}:{ES_PORT}'
    # TODO, use regex to check to make sure es_url contains an es_host too
    if es_url:
        es_index_url = f'{es_url}/{es_index}' if es_index else es_url
        try:
            response = requests.get(es_index_url, timeout=3)
            log.debug(f'ElasticSearch Server Replied: {response.json()}')
        except requests.ConnectTimeout:
            log.info(f"ConnectTimeout while trying to connect to {es_index_url}...")
            return None
        except requests.ConnectionError:
            log.info(f"Unable to connect to {es_index_url}...")
            return None
        except requests.Timeout:
            log.info(f"Timeout while trying to connect to {es_index_url}...")
            return None
        except requests.exceptions.InvalidURL:
            log.info(f"Invalid URL: {es_index_url}...")
            return None
    return es_url


ES_URL = check_es_url()
ES_HOST = None if ES_URL is None else ES_HOST
