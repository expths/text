from selenium import webdriver
from selenium.webdriver.firefox.options import Options


li = [
    "webdriver",
    "__driver_evaluate",
    "__webdriver_evaluate",
    "__selenium_evaluate",
    "__fxdriver_evaluate",
    "__driver_unwrapped",
    "__webdriver_unwrapped",
    "__selenium_unwrapped",
    "__fxdriver_unwrapped",
    "_Selenium_IDE_Recorder",
    "_selenium",
    "calledSelenium",
    "_WEBDRIVER_ELEM_CACHE",
    "ChromeDriverw",
    "driver-evaluate",
    "webdriver-evaluate",
    "selenium-evaluate",
    "webdriverCommand",
    "webdriver-evaluate-response",
    "__webdriverFunc",
    "__webdriver_script_fn",
    "__$webdriverAsyncExecutor",
    "__lastWatirAlert",
    "__lastWatirConfirm",
    "__lastWatirPrompt",
    "$chrome_asyncScriptInfo",
    "$cdc_asdjflasutopfhvcZLmcfl_"
]

options = Options()
options.add_argument('--allow-insecure-localhost')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--proxy-server=127.0.0.1:8080')
options.accept_insecure_certs = True


driver = webdriver.Firefox(options=options)
for i in li:
    ret = driver.execute_script(f"return String({i})")
    print(ret)

driver.get('https://google.com')

input(":")

driver.quit()