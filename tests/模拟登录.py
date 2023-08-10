from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
import time
"""
    url：https://www.tianyancha.com/
    测试登录并滑动获取cookie信息
"""
driver = webdriver.Chrome()
driver.get('https://www.tianyancha.com/')
driver.find_element(by="xpath", value='//*[@id="page-container"]/div[1]/div/div[1]/div[2]/div/div[5]/span').click()
time.sleep(1)
driver.find_element(by="xpath", value='//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[2]').click()
time.sleep(1)
driver.find_element(by="xpath", value='//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]').click()
time.sleep(1)

# 定位到用户名输入框并输入文本
element = driver.find_element(by="xpath", value='//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/input')
element.send_keys(15201443697)
time.sleep(2)
element = driver.find_element(by="xpath", value='//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/input')
element.send_keys("1234qwer")
time.sleep(1)
# 勾选同意
driver.find_element(by="xpath", value='//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[3]/input').click()
time.sleep(1)
# 点击登录
driver.find_element(by="xpath", value='//*[@id="J_Modal_Container"]/div/div/div[2]/div/div[2]/div/div/div[3]/div[2]/button').click()
time.sleep(2)

# 找到滑块的位置
slider = driver.find_element(By.CSS_SELECTOR,'body > div.gt_holder.gt_popup.gt_animate.gt_show > div.gt_popup_wrap > div.gt_popup_box > div.gt_slider > div.gt_slider_knob.gt_show')

driver.find_element(by="xpath", value='/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]').screenshot("../down/img/003.png")
slider.click()
time.sleep(4)

# 26块
driver.find_element(by="xpath", value='/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/div[1]').screenshot("../down/img/003_yy.png")

# 滑动注释
# action = ActionChains(driver)
# action.click_and_hold(slider).perform()
# action.move_by_offset(200, 0).perform()
# action.release().perform()

time.sleep(10)
driver.quit()
# action = ActionChains(driver)
# action.click_and_hold(slider).perform()
# action.move_by_offset(200, 0).perform()
# action.release().perform()
#
# time.sleep(5)
# driver.quit()