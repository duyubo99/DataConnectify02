# -*- codeing = utf-8 -*-
# @Time : 2023-08-11 13:54
# @Autohor : Mr.du
# @File : constants.py
# @Software : PyCharm
import os
"""
    常量定义
"""
class Constants:
    # 工程根目录路径
    PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..")).replace("\\", "/")
    # 输出日志路径
    PROJECT_LOG_PATH = PROJECT_PATH+"/logs"



if __name__ == '__main__':
    print(Constants.PROJECT_PATH)
    print(Constants.PROJECT_LOG_PATH)