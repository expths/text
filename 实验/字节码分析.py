import dis
import types


###################### 反编译字节码 ##############################
def a():
    """
    https://python3-cookbook.readthedocs.io/zh-cn/latest/c09/p25_disassembling_python_byte_code.html
    """
    n = 0
    for i in range(1000):
        n += i
    return n

def b():
    return sum(range(1000))

# print("a函数的字节码")
# dis.dis(a)

# print("b函数的字节码")
# dis.dis(b)


###################### 构建代码对象 ###############################

def f(x, y):
    return x + y

# 代码对象
c = f.__code__

# Make a completely new code object with bogus byte code
newbytecode = b'|\x00|\x01\x18\x00S\x00'
nc = types.CodeType(c.co_argcount, c.co_posonlyargcount, c.co_kwonlyargcount,
    c.co_nlocals, c.co_stacksize, c.co_flags, newbytecode, c.co_consts,
    c.co_names, c.co_varnames, c.co_filename, c.co_name,
    c.co_firstlineno, c.co_lnotab)

print("\n")
print("函数的代码对象",c)
print("函数的字节码",c.co_code)

print("\n")
print("构建的代码对象",nc)
print("构建的字节码",newbytecode)

print("\n")
print("原函数 2+3=",f(2,3))
dis.dis(f)

print("\n")
f.__code__ = nc
print("新函数 2-3=",f(2,3))
dis.dis(f)

