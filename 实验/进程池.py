
from multiprocessing.pool import Pool


def main(n):
    print("start")
    for i in range(10000):
        [x*i for x in range(i)]
    print("end")


if __name__ == "__main__":
    p = Pool(8)
    res = list()
    for i in range(1000):
        res.append(p.apply_async(main, (i,)))
    p.close()
    p.join()
