# -*- coding: utf-8 -*-

import requests
import time
import datetime
import notify
import _thread

# ----------------------------------------------------------------------------------------------------------------------
# 这里定义一些全局变量
# ----------------------------------------------------------------------------------------------------------------------

trade_flag = 0

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

vl_tr  = open("trade_bill.txt", "w")  #

# ----------------------------------------------------------------------------------------------------------------------
# 这里定义一些函数
# ----------------------------------------------------------------------------------------------------------------------

# 字符串转float型
def as_num(x):
    y = '{:.8f}'.format(x)
    return (y)

# 初始化交易币列表
def f_init_symbols_list():
    global vl_symbols_list
    vl_symbols_list = []
    for i in range(vl_len_symbols):
        vl_symbols_list.append(data[i]["symbol"])
    # print(len(vl_symbols_list))
    # print(vl_symbols_list)

# 初始化eth 交易对列表
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

# 初始化交易对 实时记录 字典列表
def f_init_dict():
    global dict
    global vl_eth_symbols_list
    dict = {}
    dict = dict.fromkeys(vl_eth_symbols_list, [0, 0, 0, 0, 0])
    print(dict)

# 实时更新交易对 价格, 只刷新每个交易对 最新的5次价格， 供算法分析之用
def f_update_dict_rtc_price():
    global vl_eth_symbols_list
    global dict
    keys_list = dict.keys()
    # print(keys_list)
    # print(vl_eth_symbols_list)
    # print(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
    # for i in range(len(keys_list)):
    # for i in range(int(len(keys_list))): # debug point
    for i in range(int(len(keys_list)/50)):
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


def f_trade(symbol, value):

    print("Enter thread f_trade -------------------------------------------------------")
    print("symbol = " + symbol)
    print("value = " + str(value))
    #print("index = " + str(index))   # debug point
    global vl_tr

    # --------------------------------------------------------------------------
    # 下单
    # --------------------------------------------------------------------------
    # TODO : 买入
    vl_tr.write("买入:"+symbol)
    vl_tr.write("  ")
    vl_tr.write(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
    vl_tr.write("  ")
    vl_tr.write(str(value))
    vl_tr.write("  \n")
    vl_tr.flush()
    # ----------------------
    # 钉钉通知
    # ----------------------
    vl_output = "买入" + symbol + " " + time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())) + " " + str(value)
    notify.send_dingding_message(vl_output)

    start_time = datetime.datetime.now()

    # --------------------------------------------------------------------------
    # 监听、卖出 算法
    # --------------------------------------------------------------------------
    # TODO + 执行卖出 操作
    while 1:
        # 获取当前值
        try:
            url = "https://api.huobi.br.com/market/history/kline?period=1min&size=2000&symbol=" + symbol
            resp = requests.get(url)
            r_json = resp.json()
            data = r_json['data']
            rc = data[0]
            rc = as_num(rc["close"])
            # 执行下单-卖出
            # TODO
            print(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))

            #根据当前值进行算法分析

            # 对时间进行判断
            end_time = datetime.datetime.now()
            diff_sec = (end_time - start_time).seconds

            if diff_sec < 300 :
                if rc > value*1.03:
                    print("卖出")
                    vl_tr.write("卖出 " + symbol + " ")
                    vl_tr.write(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
                    vl_tr.write("   价格:"+str(rc))
                    vl_tr.write(" 百分比= " + str((float(rc) - float(value)) / float(value)))
                    fo.write("  \n")
                    vl_tr.flush( )

                    vl_output = "买出" + symbol + " " + time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())) + " " + str(rc)
                    notify.send_dingding_message(vl_output)

                    trade_flag = 0
                    exit()
            else:
                print("卖出")
                vl_tr.write("卖出 " + symbol + " ")
                vl_tr.write(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
                vl_tr.write("   价格:" + str(rc))
                vl_tr.write(" 百分比= " + str((float(rc) - float(value))/float(value)))
                fo.write("  \n")
                vl_tr.flush( )
                vl_output = "买出 " + symbol + " " + time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())) + " " + str(rc)
                notify.send_dingding_message(vl_output)
                trade_flag = 0
                exit()
        except:
            print("except 下单故障 " + symbol)
            trade_flag = 0
            exit( )
        time.sleep(10)



    # 退出 线程





# 算法分析1
def f_algorithm_1( ):
    global vl_eth_symbols_list
    global dict
    global fo
    global trade_flag
    keys_list = dict.keys()

    # 每一次循环， 针对每一个交易对的5个记录，进行算法处理.
    print("Enter function f_algorithm -------------------------------------------------------")
    for i in range(len(keys_list)):
        # step 1: 读取当前交易对的 5个值

        value = dict[vl_eth_symbols_list[i]]

        # step 2:进行逻辑判断

        if float(value[0]) < float(value[1]) and float(value[1]) < float(value[2]) and float(value[2]) < float(value[3]) and float(value[3])<float(value[4]):  # debug point
            if float(value[0]) * 1.05 < float(value[4]):  # 1.05
                if float(value[0]) != 0:  # 过滤掉此处情况  [0] = 0   [1] [2] [3] [4]----> 递增 , 至此分支判断也满足时， 表示，进入交易状态
                    # --------------------------------------------------------------------------
                    # 写入本地文件，进行记录
                    # --------------------------------------------------------------------------
                    fo.write(vl_eth_symbols_list[i])
                    fo.write("  ")
                    fo.write(time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())))
                    fo.write("  ")
                    fo.write(str(dict[vl_eth_symbols_list[i]]))
                    fo.write("  \n")
                    fo.flush()
                    # --------------------------------------------------------------------------
                    # 钉钉通知
                    # --------------------------------------------------------------------------
                    vl_output = vl_eth_symbols_list[i] + " " + time.strftime('%Y.%m.%d %H %M %S', time.localtime(time.time())) + " " + str(dict[vl_eth_symbols_list[i]])
                    notify.send_dingding_message(vl_output)
                    # --------------------------------------------------------------------------
                    # 进行交易命令
                    # --------------------------------------------------------------------------
                    # 判断是否进入买入状态, 如果已经处于买入状态 ， 则不再进行买入操作。如果没有买入，则进行买入
                    if trade_flag == 0:
                        print("创建线程 " + vl_eth_symbols_list[i])
                        _thread.start_new_thread(f_trade, (vl_eth_symbols_list[i], value[4],))  # 参数1：交易对名称， 叁数2:当前价格， 参数3：在字典中的索引
                        trade_flag = 1








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
