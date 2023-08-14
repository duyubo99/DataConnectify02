# -*- codeing = utf-8 -*-
# @Time : 2023-08-11 15:05
# @Autohor : Mr.du
# @File : tianyancha.py
# @Software : PyCharm
import logging

from selenium import webdriver
from selenium.common import NoSuchElementException, InvalidCookieDomainException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from datetime import datetime
from utils.constants import Constants
from utils.image.slider_recognizer import SliderRecognizer
import json
from selenium.webdriver.chrome.options import Options
from utils.my_logger import MyLogger

"""
    登录
"""
class TianYanCha:
    def __init__(self):
        # 获取当前时间，并将其格式化为指定的字符串格式
        current_time = datetime.now().strftime('%Y-%m-%d')
        # 拼接带有时间的日志文件名称
        log_file = f'{Constants.PROJECT_LOG_PATH}/TianYanCha_{current_time}.log'

        self.logger = MyLogger(log_file)

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)  # 显示等待页面加载完成找到元素才进入下一步，这块配置全局生效
        self.baseurl = "https://www.tianyancha.com/"
        self.cookies = None
        self.login_cnt = 3 # 登录重试次数
        self.login_num = 1 # 当前登录次数
        self.init_login = False
        self.tyc_cookies = f"{Constants.PROJECT_PATH}/ceche/tyc_cookies.json"
        if not self.cookie():  # 判断本地cookie失效或没有cookie文件就返回FALSE则再次登录
            self.login()
            self.init_login = True


    def login(self):
        self.driver.get(self.baseurl)
        dl = self.driver.find_element(by="xpath", value='//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div/div[5]/span')

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

        image1_path = f"{Constants.PROJECT_DOWN_IMG_PATH}/yzm01.png"
        image2_path = f"{Constants.PROJECT_DOWN_IMG_PATH}/yzm02.png"

        time.sleep(1)
        self.driver.find_element(by="xpath",value='/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]').screenshot(image1_path)
        slider.click()
        time.sleep(4)

        # 26块
        self.driver.find_element(by="xpath",value='/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]').screenshot(
            image2_path)

        # 滑块识别，返回游标
        cursor = SliderRecognizer.find_slider_cursor(image1_path, image2_path)
        self.logger.info(f"[登录]滑块破解，游标[cursor]:{cursor}")

        cookies = self.driver.get_cookies()
        # 执行滑动
        action = ActionChains(self.driver)
        action.click_and_hold(slider).perform()
        action.move_by_offset(cursor * 10 - 15, 0).perform()
        time.sleep(2)
        action.release().perform()
        time.sleep(2)

        # 判断是否登录成功
        if self.check_login() is False:
            if self.login_num <= self.login_cnt:
                self.logger.info(f"[登录]失败，重试{self.login_num}次，最大重试次数：{self.login_cnt}")
                self.login_num += 1
                self.login()
            else:
                self.logger.info(f"[登录]失败，超过最大重试次数{self.login_cnt}次")
                self.driver.quit()
                self.logger.info(f"本次运行结束\n")
                exit()
            return


        self.logger.info(f"[登录]成功，持久化cookie")
        self.cookies = self.driver.get_cookies()
        with open(self.tyc_cookies, 'w') as f:
            json.dump(self.cookies, f)

    # 检查登录状态
    def check_login(self):
        try:
            dl = self.driver.find_element(by="xpath",
                                      value='//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div/div[5]/div/a/span')
            if dl.text != "登录/注册":
                return True
        except NoSuchElementException:
            pass

        try:
            dl = self.driver.find_element(by="xpath",
                                      value='//*[@id="page-header"]/div/div[3]/div/div[5]/div/a/span')
            if dl.text != "登录/注册":
                return True
        except NoSuchElementException:
            pass

        return False

    def cookie(self):
        self.logger.info(f"[登录]获取缓存cookie")
        if os.path.exists(self.tyc_cookies):  # 判断这个文件是否存在
            with open(self.tyc_cookies, 'r') as f:
                self.cookies = json.load(f)
            self.logger.info(f"[登录]缓存cookie获取成功")
            return True
        else:
            self.logger.info(f"[登录]无缓存cookie，开始模拟登录")
            return False

    """
        发送请求，伪装cookie信息
    """
    def setCookieToUrl(self,url):
        self.driver.get(url)
        for cookie in self.cookies:
            try:
                self.driver.add_cookie(cookie)
            except InvalidCookieDomainException:
                self.logger.info(f"[登录]无效的 cookie 域名: {cookie['domain']}")
        self.driver.get(url)
        time.sleep(2)


if __name__ == '__main__':

    url = "https://www.tianyancha.com/search?key=%E9%87%8D%E5%BA%86%E9%A9%AC%E9%87%8C%E5%A5%A5%E6%B3%A2%E7%BD%97%E8%BF%9B%E5%87%BA%E5%8F%A3%E8%B4%B8%E6%98%93%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8"

    collector = TianYanCha()
    # 无缓存的首次登录，不需要检查
    if collector.init_login is False:
        collector.logger.info(f"[登录]发送请求，伪装cookie信息")
        collector.setCookieToUrl(url)
        collector.logger.info("[登录]验证cookie有效性")
        if collector.check_login() is False:
            collector.logger.info(f"[登录]验证cookie失效，开始模拟登录...")
            collector.login()

    collector.logger.info(f"[登录]验证通过")
    # 深度采集 ==> 自动跳转登录页面(被动登录，抛异常) ==>  执行登录 ==> 深度采集
    collector.logger.info(f"开始采集数据，请求地址：{url}")
    # collector.getinfo(url)
    collector.logger.info(f"本次运行结束\n")


    collector.driver.quit()

    # dl = self.driver.find_element(by="xpath", value="//*[@id='J_NavTypeLink']")
    # if dl.accessible_name != "登录/注册":
    #     print("登录错误")
    #     self.driver.quit()
    #     return