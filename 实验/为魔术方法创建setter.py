
from typing import Any


class A():
    """
    python中魔术方法的本质是一个宏。

    调用对象的call魔术方法时，实质上是搜索并调用名为__call__的属性。
    """

    def call(self, *args: Any, **kwds: Any) -> Any:
        print("魔术方法call")

    @property
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print("被添加getter的魔术方法call")
        return self.call

if __name__ == "__main__":
    a = A()
    a.__call__
    a()