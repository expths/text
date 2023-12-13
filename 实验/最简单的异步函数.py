
import asyncio


async def add(a,b):
    return a+b

async def main():
    a = add(2,3)
    task1 = asyncio.create_task(a)#向任务簿中加入一个任务
    ret1 = await task1#取出任务的结果，如果期约未完成就会阻塞
    print(ret1)

asyncio.run(main())