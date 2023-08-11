# -*- codeing = utf-8 -*-
# @Time : 2023-08-11 15:05
# @Autohor : Mr.du
# @File : tianyancha.py
# @Software : PyCharm
import logging

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time
from utils.image.slider_recognizer import SliderRecognizer

"""
    登录
"""
class TianYanCha:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.baseurl = "https://www.tianyancha.com/"

    def login(self):
        self.driver.get(self.baseurl)
        dl = self.driver.find_element(by="xpath", value='//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div/div[5]/span')
        if dl.text != "登录/注册":
            print("登录错误")
            self.driver.quit()
            return

        # 右上角：切换登录
        xpath1 = '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[2]'
        # 选择密码登录
        xpath2 = '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]'
        # 定位到用户名输入框
        xpath3 = '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/input'
        # 定位到密码输入框
        xpath4 = '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/input'
        # 勾选同意
        xpath5 = '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[3]/input'
        # 点击登录
        xpath6 = '//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/button'



        dl.click()
        time.sleep(1)

        self.driver.find_element(by="xpath",value=xpath1).click()
        time.sleep(1)
        self.driver.find_element(by="xpath",value=xpath2).click()
        time.sleep(1)

        # 定位到用户名输入框并输入文本
        element = self.driver.find_element(by="xpath",value=xpath3)
        element.send_keys("15201443697")
        time.sleep(2)
        element = self.driver.find_element(by="xpath",value=xpath4)
        element.send_keys("1234qwer")
        time.sleep(1)
        # 勾选同意
        self.driver.find_element(by="xpath",value=xpath5).click()
        time.sleep(1)
        # 点击登录
        self.driver.find_element(by="xpath",value=xpath6).click()
        time.sleep(2)

        # 找到滑块的位置
        slider = self.driver.find_element(By.CSS_SELECTOR,
                                          'body > div.gt_holder.gt_popup.gt_animate.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show')

        image1_path = "../../down/img/001.png"
        image2_path = "../../down/img/001_yy.png"

        self.driver.find_element(by="xpath",value='/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]').screenshot(image1_path)
        slider.click()
        time.sleep(4)

        # 26块
        self.driver.find_element(by="xpath",value='/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]').screenshot(
            image2_path)

        # 滑块识别，返回游标
        cursor = SliderRecognizer.find_slider_cursor(image1_path, image2_path)
        print(f"cursor:{cursor}")

        # 执行滑动
        action = ActionChains(self.driver)
        action.click_and_hold(slider).perform()
        action.move_by_offset(cursor * 10 - 15, 0).perform()
        time.sleep(2)
        action.release().perform()
        time.sleep(2)

    """
        根据公司名称爬取深度信息
    """
    def getinfo(self,url):
        self.driver.get(url)


if __name__ == '__main__':

    url = "https://www.tianyancha.com/search?key=%E9%87%8D%E5%BA%86%E9%A9%AC%E9%87%8C%E5%A5%A5%E6%B3%A2%E7%BD%97%E8%BF%9B%E5%87%BA%E5%8F%A3%E8%B4%B8%E6%98%93%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"

    collector = TianYanCha()
    try:
        # 深度采集 ==> 自动跳转登录页面(被动登录，抛异常) ==>  执行登录 ==> 深度采集
        collector.getinfo(url)
    except NoSuchElementException:
        logging.info("无法找到元素,登录异常")
        collector.login()
        collector.getinfo(url)

    time.sleep(10)
    collector.driver.quit()

    # dl = self.driver.find_element(by="xpath", value="//*[@id='J_NavTypeLink']")
    # if dl.accessible_name != "登录/注册":
    #     print("登录错误")
    #     self.driver.quit()
    #     return