from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_articles_every_monday_8:00': {
        'task': 'news.tasks.my_job',
        'schedule': crontab(day_of_week='monday', minute=0, hour=8),
        # раз в минуту         'schedule': crontab(),
    },
}
