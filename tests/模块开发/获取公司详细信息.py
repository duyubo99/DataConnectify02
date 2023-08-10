"""
    url：https://www.tianyancha.com/
    测试根据名称检查获取深度信息

User-Agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


import time

# 重庆繁盛机电技术进出口有限公司
# 瑞幸咖啡（重庆）有限公司
# 尚哒优品商贸有限公司
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
cam_name='重庆繁盛机电技术进出口有限公司'
driver = webdriver.Chrome()





def close():
    # 关闭浏览器
    driver.quit()


def getDetailPage():
    # 打开首页
    driver.get("https://www.tianyancha.com/")
    # 输入公司名称 //*[@id="page-container"]/div[1]/div/div[3]/div[2]/div[1]/div/input
    element = driver.find_element(by="xpath",
                                  value='//*[@id="page-container"]/div[1]/div/div[3]/div[2]/div[1]/div/input')
    element.send_keys(cam_name)

    # 点击查询 //*[@id="page-container"]/div[1]/div/div[3]/div[2]/div[1]/button
    driver.find_element(by="xpath", value='//*[@id="page-container"]/div[1]/div/div[3]/div[2]/div[1]/button').click()

    time.sleep(2000)

    # 点击第一个查询到的 //*[@id="page-container"]/div/div[2]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/a/span
    driver.find_element(by="xpath",
                        value='//*[@id="page-container"]/div/div[2]/section/main/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/a/span').click()
    time.sleep(2)

    html_source = driver.page_source

    # 将HTML源代码保存到本地文件
    with open("../../down/txt/page.html", "w", encoding="utf-8") as file:
        file.write(html_source)

    # 使用BeautifulSoup解析HTML
    # soup = BeautifulSoup(html_source, 'html.parser')
    #
    # title = soup.find('title').text
    # print("页面标题：", title)
    time.sleep(10)

if __name__ == '__main__':
    getDetailPage()
    close()