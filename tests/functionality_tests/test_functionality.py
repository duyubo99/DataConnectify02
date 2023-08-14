import unittest
from PIL import Image
import os

from utils.constants import Constants
from utils.image.slider_recognizer import SliderRecognizer
from utils.my_logger import MyLogger

"""
    单元测试
"""
class TestFunctionality(unittest.TestCase):

    def test_compare_pixels(self):
        image1_path = f"{Constants.PROJECT_PATH}/down/img/001.png"
        image2_path = f"{Constants.PROJECT_PATH}/down/img/001_yy.png"
        print(image1_path)
        # 用于测试compare_pixels函数的单元测试
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        unit_type = "P"
        n = 5
        m = None

        similarities, _, _, _ = SliderRecognizer.compare_pixels(image1, image2, unit_type, n, m)



    def test_find_slider_cursor(self):
        # 用于测试find_slider_cursor函数的单元测试
        image1_path = f"{Constants.PROJECT_PATH}/down/img/001.png"
        image2_path = f"{Constants.PROJECT_PATH}/down/img/001_yy.png"

        cursor = SliderRecognizer.find_slider_cursor(image1_path, image2_path)
        print(f"cursor:{cursor}")

    def test_other_module(self):
        # 对其他功能模块进行单元测试
        # ...
        pass
    def test_log(self):
        logger1 = MyLogger("log_file1.log")
        logger2 = MyLogger("log_file2.log")

        logger1.info("This is a message to log_file1.log")
        logger2.info("This is a message to log_file2.log")


if __name__ == "__main__":
    unittest.main()