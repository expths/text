import subprocess
import asyncio
from typing import Iterable, Iterator

async def main():
	a = subprocess.Popen(["powershell"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
	a.stdin.write("pwd".encode())
	print("a")
	#a.stdin.close()
	print(a.stdout.read().decode("gbk"))
	a.stdout.close()
	a.stdin.write(b"ls")
	print(a.poll())

isinstance("",Iterable)
Iterator

asyncio.run(main())
"powershell Add-Type -Assembly PresentationCore"