import asyncio
from datetime import timedelta

import httpx
from celery import Celery
from celery.utils.log import get_task_logger

from src.core.settings import settings

app_celery = Celery('sync_db')
app_celery.conf.update(
    broker_url=settings.rabbit_url, broker_connection_retry_on_startup=True
)
app_celery.conf.result_backend = 'rpc://'
app_celery.conf.beat_schedule = {
    'sync_excel_to_db': {
        'task': 'sync_db',
        'schedule': timedelta(seconds=15),
    }
}
celery_logger = get_task_logger(__name__)


async def parse_excel_task() -> dict[str, str] | str | None:
    try:
        async with httpx.AsyncClient() as client:
            celery_logger.info('sync_db')
            response = await client.post(
                'http://resto_back:8000/api/v1/update_from_excel'
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        celery_logger.error(f'HTTP error: {e}')
        return None
    except Exception as e:
        celery_logger.error(f'Error: {e}')
        return str(e)


@app_celery.task(name='sync_db')
def sync_excel_task() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_excel_task())
