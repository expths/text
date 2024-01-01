# 输入代码文件，翻译其中的注释，以及函数定义中的文档字符串。

from translate import Translator
import re

translator= Translator(to_lang="zh")
pattern = re.compile('^\s*#(.+)')

def is_blank_line(s:str)->bool:
    if match := pattern.findall(s):
        print(match)
        return is_blank_line(match)
    return re.search('^\s*$',s)

def is_continuous(s1:str,s2:str)->bool:
    return bool(re.search('^\s*$',s1)or re.search('^\s*$',s2))

with open("pycrawler/settings.py",mode='r')as f:
    blank_line:bool = True
    s:str = ""

    for line in f:
        match = pattern.search(line)
        is_blank_line(line)

# print(translator.translate(match))
    

