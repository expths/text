import sys
import signal
import multiprocessing
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from celery import Celery

def Scrapy_main():
    """
    Scrapy爬虫主程序

    在Scrapy项目中settings文件是整个程序的入口。
    调用scrapy命令启动爬虫实质上就是读取Scrapy.cfg中settings的路径。
    """

    custom_settings = get_project_settings()
    custom_settings.setmodule('pycrawler.settings')

    print("创建scrapy进程")
    process = CrawlerProcess(settings=custom_settings)
    print("[Done]\n")

    print("添加爬虫")
    process.crawl('bitget_history_data')
    print("[Done]\n")

    print("开始爬取")
    process.start()
    print("[Done]")


def auto_worker(status_flag):
    """
    守护进程
    """
    while not status_flag.is_set():
        time.sleep(1)
        print("守护进程")
    pass

def signal_handler(sig, frame):
    """
    捕获操作系统信号
    """
    print("\n捕获到信号(SIGINT)，程序将退出。")
    # 可以在这里执行一些清理操作或记录日志
    sys.exit(0)

if __name__ == "__main__":
    # signal.signal(signal.SIGINT, signal_handler)

    # status_flag = multiprocessing.Event()# 信号守护进程信号
    # auto_process = multiprocessing.Process(target=auto_worker,args=(status_flag,))
    # auto_process.daemon = True
    # auto_process.start()
    # time.sleep(10)
    # status_flag.set()# 设置信号
    # auto_process.join()
