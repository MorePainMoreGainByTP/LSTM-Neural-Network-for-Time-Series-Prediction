# 获取国内股票历史数据

import requests

appid = 'c9cd070aa122b2ec3f051cc763782557'  # 神箭手appid


def get_domestic_stock(sticker_code,name, start_date, end_date):
    '''从神箭手API根据sticker_code获取指定日期范围的股票数据'''
    # api_adr = 'https://api.shenjian.io/'
    # index = 'false'
    # k_type = 'day'
    # fq_type = 'qfq'
    # params = {'appid': appid, 'code': sticker_code, 'index': index, 'k_type': k_type, 'fq_type': fq_type,
    #           'start_date': start_date, 'end_date': end_date}

    # 从网易接口获取数据
    api_adr = 'http://quotes.money.163.com/service/chddata.html'
    fields = "TOPEN;TCLOSE;HIGH;LOW;VOTURNOVER"
    tag = "0"   # 上海证券
    if sticker_code in ['000063','000066','000768','000651']:
        tag = "1"   # 深圳证券

    params = {'code': tag + sticker_code, 'start': start_date, 'end': end_date, 'fields': fields}
    r = requests.get(api_adr, params=params)

    print(r.url)
    # print(r.content)  # 二进制数据
    # print(r.text)     # 文本数据
    txt_list = r.text.split('\n')
    txt_list.reverse()
    txt_list[0] = txt_list[-1]  # 列名替换开头的空字符
    col_name = "Date,Code,Name,Open,Close,High,Low,Volume\n"
    txt_list[0] = col_name
    txt_list.pop(-1)

    dir_path = "..\\data\\"
    filename = name+"_"+sticker_code + "_stock.csv"
    with open(dir_path + filename, "w+", encoding='utf-8') as f:
        for line in txt_list:
            f.write(line)


def json_list_2_csv(json_data, file_name):
    '''将每个元素是json的list保存为csv格式文件'''
    with open(file_name, "w+") as f:
        column_name = ['date', 'open', 'close', 'high', 'low', 'volume']
        # 写入列名
        for each in column_name:
            if each == 'volume':
                f.write(each.title() + "\n")
            else:
                f.write(each.title() + ",")

        for each in json_data:
            for key, value in each.items():
                if key != 'code':
                    if key == 'volume':
                        f.write(value + "\n")
                    else:
                        f.write(value + ",")


if __name__ == '__main__':
    companies = {'600718':'东软集团','000651':'格力电器','600839':'四川长虹','600320':'振华重工','601988':'中国银行',
                 '000066': '中国长城','601766':'中国中车','601390':'中国中铁','000768':'中航飞机','000063':'中兴通讯'}
    sticker_code = '000066'
    start_date = '2015-06-21'  # 只能按整年获取至今日数据
    end_date = '2019-02-26'

    for code,name in companies.items():
        sticker_code = code
        get_domestic_stock(sticker_code,name, start_date, end_date)
