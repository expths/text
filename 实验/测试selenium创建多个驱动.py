from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


# 建立一个浏览器会话
driver1 = webdriver.Firefox()
executor_url = driver1.command_executor._url
session_id = driver1.session_id
driver1.get("https://duckduckgo.com/")

@(lambda f:f())
def a()->webdriver:
    # 向selenium库中注入函数
    org_command_execute = RemoteWebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    def f(executor_url)->webdriver:
        # 注入修改后的execute函数
        RemoteWebDriver.execute = new_command_execute

        newdriver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})

        # 即使不提供session_id，程序也能正常工作。
        # driver2.session_id = session_id

        # 恢复原函数
        RemoteWebDriver.execute = org_command_execute

        return newdriver
    
    return f

# 得到操作同一个浏览器的两个驱动器对象。
# 但这样做并不能多线程控制浏览器，程序和浏览器的会话始终只存在一个。
# 或许最终的接近方案依然是注入js代码。
driver2 = a(executor_url)
driver2.switch_to.new_window()
driver2.get("https://google.com")
driver1.get("https://bing.com")

# 不过这个实验也告诉了我另一件事情：selenium操作浏览器的方式是通过和executor_url的会话进行的。
# 因此如果我持有这些信息，就可以在不同主机上远程控制另一台主机上的浏览器。

print(executor_url)
print(session_id)
