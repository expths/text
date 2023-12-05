import web
import random

urls = ('/(\d*)','spider')

app = web.application(urls,globals())

page = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>web</title></head><body>

{}

</body></html>
"""
class spider():
    index = [random.randint(0,1000)for _ in range(1000)]
    def GET(self,num):
        if not num:
            return page.format(f"<h1>目录页</h1><ul>{self.get_index()}</ul>")
        num = int(num)
        return page.format(f"<h1>第{num}页</h1><p>数据：{self.get_data(num)}</p>")
    def get_data(self,num):
        return self.index[num]
    def get_index(self):
        return ''.join([f"<li><a href='/{n}'>第{n}页</a></li>"for n in range(len(self.index))])

if __name__ == "__main__":
    app.run()
