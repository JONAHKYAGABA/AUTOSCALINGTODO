from datetime import timezone
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_master.settings')

app = Celery('todo_master')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.result_backend = 'django-db'

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-notify': {
        'task': 'to_do_list.tasks.send_notification',
        'schedule': crontab(minute='*/1'),
        'args': (1,),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
