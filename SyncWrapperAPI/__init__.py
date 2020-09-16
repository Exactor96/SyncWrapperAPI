from aiohttp import web

from .config import PROXY_URLS, ASYNC_PROXY_URLS
from .views import sync_proxy, async_proxy


def get_app() -> web.Application:
    """Функция возвращает экземпляр приложения с добавленными обработчиками."""
    app = web.Application()

    for url in PROXY_URLS:
        app.add_routes([web.post(url, sync_proxy)])

    for url in ASYNC_PROXY_URLS:
        app.add_routes([web.post(url, async_proxy)])

    return app


app = get_app()
