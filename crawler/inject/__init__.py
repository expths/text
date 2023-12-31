# 将这里的脚本包装成python函数


from typing import Any
import re


class Inject_script:
    """
    将可注入浏览器的javascript脚本包装成python对象。

    使用元编程技巧，每次执行这里的代码时将脚本包装成函数写入模块文件本身。
    自动增量更新。
    """

    _check_script_name = re.compile(".json$")

    def __init__(self,script:str) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

test = Inject_script("test")