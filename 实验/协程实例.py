# 2022/8/10更新
# async声明的异步函数其实是一个协程任务生成器，调用异步函数对象会返回coroutine对象。

# 可以发现一个coroutine是有一个例程对象，而task是一个任务对象(3.10以后被移除)。
# 换言之，coroutine是尚未准备好的任务，而task则是已经加入行程的任务。
# 对象变成task意味着此时这段程序将交由控制器调度，它可能立即开始执行但不会阻塞。
# async关键字意味着新建任务，而await关键字意味着需要等待任务结果。
# 协程的所有内容都必须放入异步函数中，这意味着主函数只能是同步的（主函数只有一个）。

# 通过查询标准库文档发现，协程定义了可等待对象，一个对象如果可以在await中调用就是可等待的。
# 对于协程函数和协程对象，除了使用async以外，还可以通过生成器得到，或者说生成器就是协程函数的本质。
# 通过await调用的对象将转变为Futures对象（期约），在这个对象得到结果前将会发生阻塞。
# asyncio.run函数是整个程序的核心，它管理传入的协程直到消亡。

# 注意：
# 由于await意味着等待对应的异步函数返回值，如果代码此时才开始运行很可能会阻塞。
# 因此我们往往需要先准备好任务簿，使用asyncio模块的create_task函数（加入任务）或gather函数（并发，3.10后被移除）。

# 屏蔽取消函数shield将会使一个异步函数不会被取消。
# 超时函数wait_for会根据第二个参数传入的秒数计算时间，如果超时会被取消并引发超时错误。
# to_thread函数是高阶函数，接受函数名及其参数后在新线程中运行。

import asyncio

async def A(n:int):
    await asyncio.sleep(n)
    print(n)
    return n

async def B():
    #a = asyncio.create_task(A(3.0))
    a = asyncio.wait_for(A(3.0),1)#创建单个异步任务
    print("start")
    print(asyncio.current_task())#返回正在运行的任务
    print(asyncio.all_tasks())#返回尚未完成的任务集合
    ret = await asyncio.gather(#并发
        A(1),
        A(2),
        A(3),
        A(4)
    )
    print(ret)#gather函数会等待一系列异步函数结果
    try:
        a = await a #由于a任务早已完成，这里不会发生阻塞
        print(a)
    except asyncio.TimeoutError:#当任务超时时会引发引发超时错误，该错误会传递给期约。
        print("超时")
#
asyncio.run(B())#主函数


