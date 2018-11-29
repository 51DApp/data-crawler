from datetime import datetime, time
import time
import logging
from logging import handlers
from dappradar.get_dapp_data import get_all_eos_dapp_info
from es_tools.es_client import init_es_client

import sys

sys.path.append("..")

# 初始化logger
logger = logging.getLogger()
# 配置日志级别，如果不显示配置，默认为Warning，表示所有warning级别已下的其他level直接被省略，
# 内部绑定的handler对象也只能接收到warning级别以上的level，你可以理解为总开关
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s - %(message)s",
                              datefmt="%m-%d-%Y %I:%M:%S")  # 创建一个格式化对象

console = logging.StreamHandler()  # 配置日志输出到控制台
console.setLevel(logging.WARNING)  # 设置输出到控制台的最低日志级别
console.setFormatter(formatter)  # 设置格式
logger.addHandler(console)

# file_logging = logging.FileHandler("dappradar_to_es.log") # 配置日志输出到文件
# file_logging.setLevel(logging.WARNING)
# file_logging.setFormatter(formatter)
# logger.addHandler(file_logging)

file_time_rotating = handlers.TimedRotatingFileHandler("dappradar_to_es.log", when="D", interval=1, backupCount=5)
file_time_rotating.setLevel(logging.INFO)
file_time_rotating.setFormatter(formatter)
logger.addHandler(file_time_rotating)

es_eos_dappradar_index = 'eos_dappradar'


def get_contract_str(contracts):
    if contracts is None:
        return ''

    contracts_lists = []

    for contract in contracts:
        contracts_lists.append(contract['address'])

    return ' '.join(map(str, contracts_lists))


def get_links_dict(links):
    result_dict = {}

    for line in links:
        result_dict[line['app']] = line

    return result_dict


def date_str_to_timestamp(date_str):
    str_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

    ans_time = time.mktime(str_date.timetuple())

    return ans_time * 1000


def write_eos_dappradar_to_es():
    es_client = init_es_client()

    dapp_info_list = get_all_eos_dapp_info()

    logger.info('dapp list:' + str(len(dapp_info_list)))

    for dapp in dapp_info_list:
        try:
            info = dapp['info']
            links = dapp['links']
            contracts = dapp['contracts']

            info['updatedAt'] = date_str_to_timestamp(info['updatedAt'])
            info['createdAt'] = date_str_to_timestamp(info['createdAt'])

            index_dict = info
            index_dict['links'] = links
            index_dict['contracts'] = get_contract_str(contracts)

            id = info['id']

            res = es_client.index(index=es_eos_dappradar_index, doc_type='_doc', id=id, body=index_dict)

            logger.info('es result:' + str(res))

        except Exception as err:
            logger.error(err)


if __name__ == '__main__':
    write_eos_dappradar_to_es()
