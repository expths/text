from multiprocessing import Process
import time


def f():
	print("start")
	for i in range(10000):
		[x*i for x in range(i)]
	print("end")

print("abc") # 这里会打印两次，主进程和子进程都会被打印。

if __name__ == "__main__":
	p = Process(target=f)
	p.daemon = True # python的守护进程不同于Linux的守护进程（服务）
	p.start()
	time.sleep(5)
	exit()
