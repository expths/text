from selenium import webdriver
from selenium.webdriver.firefox.options import Options

option = Options()
driver = webdriver.Firefox(options=option)
driver.install_addon("data/ghostery-8.12.5.xpi")
driver.get("https://google.com")
driver.get("https://bing.com")