import requests


# 获取列表页信息
def request_basic_eth_dapp_page(page):
    url = "https://dappradar.com/api/dapps/list/" + str(page)
    r = requests.get(url)

    return r.text


# 获取列表页信息
def request_basic_eos_dapp_page(page):
    url = "https://dappradar.com/api/eos/dapps/list/" + str(page)
    r = requests.get(url)

    return r.json()['data']['list']


# 获取EOS DApp页面数量
def get_eos_page_count():
    url = "https://dappradar.com/api/eos/dapps/list/0"
    r = requests.get(url)
    return r.json()['data']['pageCount']


# 获取ETH DApp页面数量
def get_eth_page_count():
    url = "https://dappradar.com/api/dapps/list/0"
    r = requests.get(url)
    return r.json()['data']['pageCount']


# 获取单个eos DApp的详细信息
def get_eos_dapp_detail_info(dapp_id):
    url = 'https://dappradar.com/api/eos/dapp/' + str(dapp_id)
    r = requests.get(url)

    return r.json()['data']


# 获取所有EOS DApp的详细信息
def get_all_eos_dapp_info():
    page_count = get_eos_page_count()
    # page_count = 2

    dapp_list = []
    for page in range(0, page_count):
        result_list = request_basic_eos_dapp_page(page)
        dapp_list.extend(result_list)

    collected_dapp_info = []
    for dapp in dapp_list:
        id = dapp['id']

        detail_info = get_eos_dapp_detail_info(id)
        collected_dapp_info.append(detail_info)

        # break

    return collected_dapp_info


if __name__ == '__main__':
    # print(get_eos_page_count())
    # print(get_eth_page_count())

    # r = get_eos_dapp_detail_info(652)

    dapp_info_list = get_all_eos_dapp_info()

    for dapp in dapp_info_list:
        print(dapp)
