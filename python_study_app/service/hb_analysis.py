# -*- coding: utf-8 -*-

import requests
import time

# ----------------------------------------------------------------------------------------------------------------------
# 这里定义一些全局变量
# ----------------------------------------------------------------------------------------------------------------------


# currencys_url="https://api.huobi.br.com/market/history/kline?period=1min&size=200&symbol=xmxeth"

BASE_URL = "https://api.huobi.pro"  # 官网api文档中最新的base url

API1 = "/market/history/kline"
PARAM1 = "?period=1min&size=200&symbol=xmxeth"  # history 接口需要提供的参数
currencys_url_1 = BASE_URL + API1 + PARAM1

# 根据官网 / api doc / 获取所有交易对
API2 = "/v1/common/symbols"
currencys_url_2 = BASE_URL + API2

# 根据官网 ----> api doc
API4 = "/v1/common/currencys"  # 获取所有币种
currencys_url_4 = BASE_URL + API4

vl_symbols_list = []  # 所有交易对列表

vl_eth_symbols_list = []  # eth交易对列表

dict = {}  # 用于记录每个eth交易对，5个实时、最新的值，供不同的 algorithm用

fo = open("foo.txt", "w")  # foo.txt 记录算法结果


# ----------------------------------------------------------------------------------------------------------------------
# 这里定义一些函数
# ----------------------------------------------------------------------------------------------------------------------
def as_num(x):
    y = '{:.8f}'.format(x)
    return (y)


def f_init_symbols_list():
    global vl_symbols_list
    vl_symbols_list = []
    for i in range(vl_len_symbols):
        vl_symbols_list.append(data[i]["symbol"])
    # print(len(vl_symbols_list))
    # print(vl_symbols_list)


def f_init_eth_symbols_list():
    global vl_symbols_list
    global vl_eth_symbols_list
    vl_eth_symbols_list = []
    for i in range(vl_len_symbols):
        vl_temp = vl_symbols_list[i]
        if vl_temp[-3:] == "eth":
            if len(vl_temp) > 3:
                vl_eth_symbols_list.append(vl_temp)
    print(vl_eth_symbols_list)
    # print(len(vl_eth_symbols_list))


def f_init_dict():
    global dict
    global vl_eth_symbols_list
    dict = {}
    dict = dict.fromkeys(vl_eth_symbols_list, [0, 0, 0, 0, 0])
    print(dict)


def f_update_dict_rtc_price():
    global vl_eth_symbols_list
    global dict
    keys_list = dict.keys()
    # print(keys_list)
    # print(vl_eth_symbols_list)
    # print(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
    # for i in range(len(keys_list)):
    for i in range(int(len(keys_list))):
        try:
            url = "https://api.huobi.br.com/market/history/kline?period=1min&size=2000&symbol=" + vl_eth_symbols_list[i]
            resp = requests.get(url)
            r_json = resp.json()
            data = r_json['data']
            rc = data[0]
            rc = as_num(rc["close"])
            dict[vl_eth_symbols_list[i]] = dict[vl_eth_symbols_list[i]][1:]
            dict[vl_eth_symbols_list[i]].append(rc)
        except:
            print("except " + str(i) + " " + vl_eth_symbols_list[i])
    print(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))


def f_algorithm_1():
    global vl_eth_symbols_list
    global dict
    global fo
    keys_list = dict.keys()

    # 每一次循环， 针对每一个交易对的5个记录，进行算法处理.
    # print("-------------------------------------------------------")
    for i in range(len(keys_list)):
        # step 1: 读取当前交易对的 5个值

        value = dict[vl_eth_symbols_list[i]]

        # step 2:进行逻辑判断
        if float(value[0]) < float(value[1]) and float(value[1]) < float(value[2]) and float(value[2]) < float(value[3]) and float(value[3])<float(value[4]):
            if float(value[0]) * 1.05 < float(value[4]):  # 1.05
                if float(value[0]) != 0:  # 过滤掉此处情况  [0] = 0   [1] [2] [3] [4]----> 递增
                    fo.write(vl_eth_symbols_list[i])
                    fo.write("  ")
                    fo.write(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
                    fo.write("  ")
                    fo.write(str(dict[vl_eth_symbols_list[i]]))
                    fo.write("  \n")
                    fo.flush()


# ----------------------------------------------------------------------------------------------------------------------
# main 函数
# ----------------------------------------------------------------------------------------------------------------------
while 1:

    resp = requests.get(currencys_url_2)
    r_json = resp.json()
    data = r_json['data']

    vl_len_symbols = len(data)
    print("总交易对个数:" + str(vl_len_symbols))

    # step 1: 初始化交易对列表
    f_init_symbols_list()

    # step 2: 初始化eth交易对列表
    f_init_eth_symbols_list()

    # step 3: 初始化字典， 字典每个key, 的value 是10个最新的 价格
    f_init_dict()

    # step 4: while 50秒更新一次值, dict{key:value,  key:value, key:value  ......} ->保存最新的5分钟内的值，
    #         每次更新之后，根据5分钟之内的数据，掉用相应的算法，进行建模、计算
    while 1:
        f_update_dict_rtc_price()
        f_algorithm_1()

    time.sleep(6)
