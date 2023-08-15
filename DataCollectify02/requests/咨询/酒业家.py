# -*- codeing = utf-8 -*-
# @Time : 2023-08-15 9:34
# @Autohor : Mr.du
# @File : 酒业家.py
# @Software : PyCharm
# https://api.jiuyejia.com/news/news/v2/search?current=1&size=10000&keyword=洋酒
# 根据ID拿到内容：https://api.jiuyejia.com/news/news/117048

import requests
from w3lib.html import replace_entities
from w3lib.html import remove_tags
from datetime import datetime
from utils.constants import Constants
from utils.my_sql_tool import MySQLTool

# 创建 MySQLTool 实例
tool = MySQLTool(config_file=f'{Constants.PROJECT_CONFIG_PATH}/database_config.ini')

# 连接到数据库
database = 'local'
tool.connect(database)

# 定义要写入的表名和列名
table = 'wine_consultation'
columns = ['src_id', 'src_title', 'src_publishTime', 'src_parentTagCode', 'src_score', 'src_coverImg', 'src_author', 'src_sourceName', 'cleaned_content', 'search_keyword', 'res_total', 'req_time']

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 定义请求信息
url = "https://api.jiuyejia.com/news/news/v2/search"
keyword = "红酒"
param = {
    "current": "1",
    "size": "1000",
    "keyword": f"{keyword}"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
}

resp = requests.get(url,params=param,headers=headers)
# print(resp.request.url)
records = resp.json()['data']['records']

values_to_insert = []
for item in records:
    values = [
        item['id'],
        remove_tags(item['title']),
        item['publishTime'],
        item['parentTagCode'],
        item['score'],
        item['coverImg'],
        item['author'],
        item['sourceName']
    ]

    # print(item['id'])
    # print(remove_tags(item['title']))
    # print("===========")
    # print(item['publishTime'])
    # print(item['parentTagCode'])
    # print(item['score'])
    # print(item['coverImg'])
    # print(item['author'])
    # print(item['sourceName'])

    # 根据ID拿到内容：https://api.jiuyejia.com/news/news/155985
    if item['id'] is not None:
        url_detail = f"https://api.jiuyejia.com/news/news/{item['id']}"
        resp2 = requests.get(url_detail, headers=headers)
        content = resp2.json()['data']['content']
        # print(content)
        cleaned_content = replace_entities(remove_tags(content)).replace(" ", "").replace("\n", "")
        # print(cleaned_content)
        values.append(cleaned_content)
        # values.append(content)
        # print(values)
    # 查询标签值
    values.append(keyword)
    # 反回记录条数
    values.append(resp.json()['data']['total'])
    # 请求时间
    values.append(current_time)

    values_to_insert.append(values)
# print(values_to_insert)

# 执行批量插入操作
tool.execute_insert(database, table, columns, values_to_insert)

# print(resp.json()['data']['records'])
print(f"总条数：{resp.json()['data']['total']}，请求总条数：{param['size']}")
resp.close()
# 断开与数据库的连接
tool.disconnect(database)



# CREATE TABLE IF NOT EXISTS `wine_consultation` (
#    `src_id` VARCHAR(255),
#    `src_title` VARCHAR(255),
#    `src_publishTime` VARCHAR(255),
#    `src_parentTagCode` VARCHAR(255),
#    `src_score` VARCHAR(255),
#    `src_coverImg` VARCHAR(255),
#    `src_author` VARCHAR(255),
#    `src_sourceName` VARCHAR(255),
#    `cleaned_content` TEXT,
#    `search_keyword` VARCHAR(255),
#    `res_total` INT,
#    `req_time` VARCHAR(64)
#  );

