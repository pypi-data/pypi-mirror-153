from delphai_utils.logging import logging
from delphai_utils.config import get_config
from elasticsearch import AsyncElasticsearch

logging.getLogger("elasticsearch").setLevel(logging.ERROR)
es_host = get_config("elasticsearch.host")
es_index = get_config("elasticsearch.index")
es_username = get_config("elasticsearch.username")
es_password = get_config("elasticsearch.password")
es_port = get_config("elasticsearch.port")
es_address = es_host
if not es_address.startswith("https://"):
    es_address = f"http://{es_host}:{es_port or 80}"
es = AsyncElasticsearch(
    hosts=[es_address], http_compress=True, http_auth=(es_username, es_password)
)
