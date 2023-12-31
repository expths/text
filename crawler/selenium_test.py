from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException,WebDriverException
import json

cookies_file = "cookies/binance.json"
options = webdriver.FirefoxOptions()
options.add_argument("--auto-open-devtools-for-tabs")
driver = webdriver.Firefox(options=options)

# 设置等待元素的时间
driver.implicitly_wait(2)

# 前往域
driver.get('https://www.binance.com')

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
