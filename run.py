import uvicorn

from src import create_app
from src.services.cache_service import CacheService

app = create_app()


@app.on_event('shutdown')
async def shutdown() -> None:
    """ Clear cache after app shutdown."""
    service = CacheService()
    await service.flush_redis()

if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True)
