from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException,WebDriverException
import json
import re
from time import sleep
from random import random
import pyotp

cookies_file = "cookies/binance.json"
Authenticator = pyotp.parse_uri("")
options = webdriver.FirefoxOptions()
options.add_argument("--auto-open-devtools-for-tabs")
driver = webdriver.Firefox(options=options)

# 设置等待元素的时间
driver.implicitly_wait(2)

# 前往根域
driver.get('https://binance.com')

def bcap():
    try:
        driver.find_element(By.XPATH,'//div[class="bcap-modal"]')
        input("等待人机验证:")
    except:
        pass

def wait():
    sleep(1+3*random())

try:
    # 读取所有cookies
    with open(cookies_file,'r')as json_file:
        cookies = json.loads(json_file.read())
        list(map(driver.add_cookie,cookies))
except FileNotFoundError:
    # 缺失cookies文件
    pass
except json.decoder.JSONDecodeError:
    # 空文件
    pass

driver.get('https://www.binance.com')

# 登录
def login():
    try:
        d = driver.find_element(By.ID,"toLoginPage")
        d.click()
    except NoSuchElementException:
        driver.get("https://www.binance.com/zh-CN/my/dashboard")
        print("已经登录")
        return

    bcap()
    wait()

    try:
        d = driver.find_element(By.ID,"username")
        d.send_keys("esp9900k@gmail.com")
    except BaseException as err:
        print("[ERR]",err)

    try:
        d = driver.find_element(By.ID,"click_login_submit_v2")
        d.click()
    except BaseException as err:
        print("[ERR]",err)

    bcap()
    wait()

    try:
        d = driver.find_element(By.XPATH,'//input[@name="password"]')
        d.send_keys("DVSiNYCQP-X5vgx")
    except BaseException as err:
        print("[ERR]",err)

    try:
        d = driver.find_element(By.ID,"click_login_submit_v2")
        d.click()
    except BaseException as err:
        print("[ERR]",err)

    bcap()
    wait()

    # input maxlength="6" inputmode="numeric"
    try:
        d = driver.find_element(By.XPATH,'//input[maxlength="6"]')
        d.send_keys(Authenticator.now())

    except BaseException as err:
        print("[ERR]",err)


# 复选框
# <div id="selected" name="selected" class="bn-checkbox bn-checkbox__square css-vurnku"><div class="bn-checkbox-icon"><svg fill="bg1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" class="bn-svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.035 16.812l-.001.002 2.121 2.121.002-.002 2.121-2.12 9.19-9.192-2.12-2.121-9.191 9.19-3.536-3.534-2.121 2.12 3.535 3.536z" fill="currentColor"></path></svg></div><div data-bn-type="text" class="css-13z70xy">不再在此设备上显示此消息</div></div>

# 按钮
# <button class="bn-button bn-button__default.flatprimary data-size-large css-xy3oy8">是</button>

login()
input(":")
bcap()
wait()
# 进入主页
tirle = re.compile("总览.*币安")
try:
    tirle.search(driver.title)

    # 资产
    d = driver.find_element(By.XPATH,'//div[@class="text-t-primary"]//div[@class="typography-Headline4"]')
    print(d.text)
    
except BaseException as err:
    print("[ERR]",err)

bcap()
wait()

# 启动网站
driver.get('https://www.binance.com/zh-CN/copy-trading/lead-details/3725468878881937408')

try:
    xpath = '//div[@class="bn-table-container"]//table//tr[@data-row-key]'
    # tab = driver.find_elements(By.XPATH,xpath)

    with open('crawler/inject/test.js',mode='r',encoding='utf-8')as script:
        script = script.read()
    
    # execute_script的输入代码会被放入容器中执行，使用return语句返回值。
    tab = driver.execute_script(script)
    print(tab)
except NoSuchElementException:
    print("找不到目标！")

# input(":")
# for i in driver.find_elements(By.XPATH,xpath):
#     print(i.get_attribute("data-row-key"))

# 等待退出
input("等待<Enter>退出:")


try:
    # 保存cookies
    # 注意包含cookie文件安全，确认已经拿到cookie后再写入文件。
    # 检验浏览器是否意外关闭
    cookies = driver.get_cookies()
except NoSuchWindowException as err:
    print("标签页丢失：",err)
except WebDriverException as err:
    print("浏览器丢失：",err)
else:
    # 保存cookies
    with open(cookies_file, 'w') as json_file:
        json.dump(cookies, json_file)

driver.quit()
