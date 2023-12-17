import re

input = """

# A

## B

### C

"""

class markdown():
    """
    markdown标签类

    块标签：
    - 标题
    - 段落
    - 列表
    - 表格
    - 代码块
    - latex表达式

    行标签
    """
    pass

def markdown_to_html(md:str)->str:
    a = re.match('\n# (.*)\n',md)
    print(a)


if __name__ == "__main__":
    markdown_to_html(input)