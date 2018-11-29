from es_tools.es_client import init_es_client
import sys

sys.path.append("..")

es = init_es_client()

res = es.get(index="eos_dappradar", doc_type='_doc', id='835', )
print(res['_source'])
