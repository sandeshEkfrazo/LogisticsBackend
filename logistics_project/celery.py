import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')

app = Celery('logistics_project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')



# Load task modules from all registered Django apps.
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print("hello im printing in celery.py file")
    
    
  
