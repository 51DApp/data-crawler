from elasticsearch5 import Elasticsearch, RequestsHttpConnection

host = 'es-cn-4590v0ixf0001ynym.public.elasticsearch.aliyuncs.com'
username = 'elastic'
password = '51DApp6666'


def init_es_client():
    """
    初始化es client
    :return: es client
    """
    es = Elasticsearch(
        [host],
        http_auth=(username, password),
        port=9200,
        use_ssl=False
    )

    return es


def init_es_proxy_client():
    """
    通过proxy连接ES，使用Shadowsocks做代理
    :return: es client
    """

    class MyConnection(RequestsHttpConnection):
        def __init__(self, *args, **kwargs):
            proxies = kwargs.pop('proxies', {})
            super(MyConnection, self).__init__(*args, **kwargs)
            self.session.proxies = proxies

    es = Elasticsearch(
        [host],
        http_auth=(username, password),
        port=9200,
        use_ssl=False,
        connection_class=MyConnection,
        proxies={'http': '127.0.0.1:1087'})

    return es
