import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')

app = Celery('logistics_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'export-database': {
        'task': 'userModule.tasks.export_database_task',
        'schedule': 10.0,  # Every 10 seconds
    },
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


    
