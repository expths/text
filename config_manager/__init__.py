import json
from typing import Any
from template import *
from configError import ConfigError

class Config():
    def __init__(self) -> None:
        """
        导入配置文件。

        如果配置文件不存在，将配置名称保存下来。
        """
        pass

    def __getattr__(self, __name: str) -> Any:
        """
        提供配置文件。

        如果请求了不存在的配置，将名称保存下来。
        """
        pass

    def __setattr__(self, __name: str, __value: Any) -> None:
        raise ConfigError("不应该在这里修改配置文件")

    def a():
        """
        创建新的配置文件。
        """

    def b():
        """
        将配置文件导入数据库。
        """

    def c():
        """
        扫瞄保存下来的异常配置请求。
        """


def read_config():
    """
    读取所有配置文件
    """
    with open("config.json",mode='r')as config_file:
        return json.load(config_file)


def read_config(file_name):
    """
    读取json文件。
    
    如果不存在则创建。
    """
    try:
        return
    except:
        create_config(file_name)

def create_config(file_name:str)->None:
    """
    创建json配置文件。
    """
    pass


def a():
    """
    检查配置文件完整性。

    读取模板配置文件,检查是否均配置完成。
    """
    pass

def b():
    """
    检查意外的配置文件
    """
    pass

def c():
    """
    编辑自身
    """
    pass

config = read_config()
BITGET_API = config["bitget_api"]
postgreSQL = config["postgreSQL"]

if __name__ == "__main__":
    print(config)
