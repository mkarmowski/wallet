import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('wallet',
             broker='amqp://',
             backend='amqp://',
             include=['wallet/transactions/tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
