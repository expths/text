import asyncio
from multiprocessing.pool import Pool


async def a(n):
    print("start",n)
    for i in range(10000):
        [x*i for x in range(i)]
    print("  end",n)

async def main():
    for i in list(map(lambda n:asyncio.create_task(a(n)),range(10))):
        print("由此开始异步函数")
        await i
    return 0

if __name__ == "__main__":
    p = Pool(8)
    res = list()
    for i in range(100):
        res.append(p.apply_async(lambda x:x))
    p.close()
asyncio.run(main())