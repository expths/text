import socket
import asyncio

destination = ("5y1311r496.qicp.vip",17511)
cont = "abcdefg"

udp_s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_s.bind(("",8080))

async def recv():
    return udp_s.recvfrom(1024)

async def main():
    a = asyncio.create_task(recv())
    udp_s.sendto(cont.encode("utf-8"),destination)
    ret = (await a)[0].decode("utf-8")
    print(ret)

asyncio.run(main())
udp_s.close()
