from selenium import webdriver
options = webdriver.FirefoxOptions()
options.add_argument("--auto-open-devtools-for-tabs")
driver = webdriver.Firefox(options=options)

driver.get('https://www.google.com')

# 检查浏览器机器人指纹
a = driver.execute_script('window')
print(a)

driver.quit()