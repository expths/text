from celery import Celery

# 重构
application = Celery(
    "cabbage",
    broker='redis://127.0.0.1',
    backend='redis://127.0.0.1',
    include=[
        'Task.test',
        # 'Task.'
        ]
    )

application.conf

print("================")
