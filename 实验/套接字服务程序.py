import socket
import asyncio
import time

# 监听套接字初始化
tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_s.bind(("", 8800))
tcp_s.listen(5)  # 设置监听模式


async def accept_request():  # 这个函数处理请求
    new_socket, client_addr = tcp_s.accept()  # 监听到请求时产生一个新的套接字
    resv_data = new_socket.recv(1024)
    print(resv_data.decode("utf-8"), "for", client_addr)
    new_socket.send(b"Hi!")
    new_socket.close()
    return 0


async def request():  # 这个函数发出请求
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(("127.0.0.1", 8800))
    tcp.send(b"Hello")  # 向自己发送信息


async def main():  # 主函数
    print("start")
    futures = asyncio.create_task(accept_request())  # 后台监听
    time.sleep(1)  # 稍等1秒
    await request()  # 发出请求
    await futures

asyncio.run(main())
tcp_s.close()
