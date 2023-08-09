# Scrapy settings for DataCollectify02 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "DataCollectify02"

SPIDER_MODULES = ["DataCollectify02.spiders"]
NEWSPIDER_MODULE = "DataCollectify02.spiders"


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


#UA伪装
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"

#禁止robots（不遵从robots协议）
ROBOTSTXT_OBEY = False

#指定日志
LOG_LEVEL = 'ERROR'

# 禁止重试
RETRY_ENABLED = False


# 配置数据源
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD ='123456'
DB_DATABASE = 'col_data'