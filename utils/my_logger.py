# -*- codeing = utf-8 -*-
# @Time : 2023-08-14 16:00
# @Autohor : Mr.du
# @File : my_logger.py
# @Software : PyCharm
import logging


class MyLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(log_file)  # 创建一个不同名称的 logger 对象
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)