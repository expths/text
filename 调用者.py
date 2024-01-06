from Celery.工作者 import add
from celery import group,chain,chord

print("\n开始程序\n")

# 直接调用add函数本身，等同于调用原函数，不会调用异步队列的功能。
a = add(2,3)
print("直接调用函数",a)
print(type(a))
print("\n")

# 使用delay方法将创建一个任务加入队列。
a = add.delay(2,3)
print("调用delay方法",a)
print(type(a))
print("返回值",a.get())
print("\n")

# delay() 实际上为 apply_async() 的快捷使用。
# apply_async方法可以输入关于任务的一系列配置。
a = add.apply_async((2,3),countdown=1)
print("调用apply_async方法",a)
print(type(a))
print("返回值",a.get())
print("\n")

# signature方法返回一个签名对象，将函数及其参数和配置打包成一个任务。
# 签名对象可以进行组合、运算、调用等复杂操作。
# 可以简写为s
task = add.signature((2,3),countdown=1)
print("调用signature方法",task)
print(type(task))
print("返回值",a.get())
print("\n")

# 签名不必包含完整的参数列表，可以先定义一部分，在未来补全。
# 签名更重要的作用是可以作为对象组合构成组、链等更复杂的任务。
group(add.s(i, i) for i in range(1000))().get()