from celery import Celery

from src.core.settings import settings

app = Celery(
    'tasks',
    broker=settings.rabbit_url,
    backend=settings.database_url
)
app.conf.beat_schedule = {
    'sync_excel_to_db': {
        'task': 'src.tasks.excel_to_db',
        'schedule': 15,
    }
}

app.autodiscover_tasks(['src.tasks'])
