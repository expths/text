import json
from typing import Any
from config_manager.configError import ConfigError


def read_config_file():
    """
    读取所有配置文件
    """
    with open("config.json",mode='r')as config_file:
        return json.load(config_file)


class Config():
    config = read_config_file()

    def __init__(self,model_name:str) -> None:
        """
        导入配置文件。

        如果配置文件不存在，将配置名称保存下来。
        """
        try:
            self.model_name = model_name
            self.config =  config[model_name]
        except:
            model_name

    def __str__(self) -> str:
        return f"<config of {self.model_name}>"

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


config = read_config_file()
BITGET_API = config["bitget_api"]
postgreSQL = config["postgreSQL"]

if __name__ == "__main__":
    print(config)
