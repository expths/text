from celery import Celery

# celery在windows上不再受到支持。

a_worker = Celery('a_tasks', broker='redis://127.0.0.1',backend='redis://127.0.0.1')
# 通过查询文档。Celery分布式调用的本质是在多个工作者进程中连接到同一个broker队列。
# 在这里就是redis服务。


print("运行工作者线程代码")
# 调用 celery -A Celery.工作者 worker -l info 启动工作者程序。
# 
#  celery@82F2 v5.3.6 (emerald-rush)
# 
# Windows-10-10.0.22621-SP0 2024-01-03 02:27:25
# - *** --- * --- 
# - ** ---------- [config]
# - ** ---------- .> app:         a_tasks:0x1f8dde4b340
# - ** ---------- .> transport:   redis://127.0.0.1:6379//
# - ** ---------- .> results:     disabled://
# - *** --- * --- .> concurrency: 8 (prefork)
# -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
# --- ***** -----
#  -------------- [queues]
#                 .> celery           exchange=celery(direct) key=celery
# [tasks]
#   . Celery.工作者.add
#
# celery默认开启了8个线程，通过任务管理器可以看见10个python进程和一个celery进程。
# 根据控制台输出还可以看见目前服务中有一个队列，命名为celery。



# 在调用者中可以直接调用add函数，无需启动工作者进程。
# 看来task装饰器方法不会直接修改程序本身的逻辑，只是在函数属性中添加了队列相关的方法。
# 
# 如果使用相对导入，会在celery中得到KeyError异常。celery找不到函数所属的模块。
# 
# 使用wsl调用celery顺利启动了服务器。
# 但这也带来了许多麻烦，因为这意味着库中的代码将会存在操作系统依赖。
# [2024-01-03 02:13:15,788: INFO/MainProcess] Connected to redis://127.0.0.1:6379//
# [2024-01-03 02:13:15,791: INFO/MainProcess] mingle: searching for neighbors
# [2024-01-03 02:13:16,871: INFO/MainProcess] mingle: all alone
# [2024-01-03 02:13:16,884: INFO/MainProcess] celery@82F2 ready.
# [2024-01-03 02:13:34,255: INFO/MainProcess] Task Celery.工作者.add[d9b8b5eb-bc8a-422e-91ea-3bfccde46cb2] received
# [2024-01-03 02:13:34,257: WARNING/ForkPoolWorker-8] 运行add函数
# [2024-01-03 02:13:34,259: INFO/ForkPoolWorker-8] Task Celery.工作者.add[d9b8b5eb-bc8a-422e-91ea-3bfccde46cb2] succeeded in 0.0025552559964125976s: 5
@a_worker.task
def add(x, y):
    print("运行add函数")
    return x + y