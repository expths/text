from cabbage import application

@application.task
def f():
    """
    在运行时向celery注入新任务 失败

    出现KeyError异常
    """
    print("开始任务")
    application.tasks['cabbage.g'] = f
    print("注入完成")