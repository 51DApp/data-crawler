from elasticsearch import es_client
from elasticsearch.es_client import init_es_client

es = init_es_client()


res = es.get(index="eos_dapp_info", doc_type='_doc', id='WAR GAME - WIZZ',)
print(res['_source'])