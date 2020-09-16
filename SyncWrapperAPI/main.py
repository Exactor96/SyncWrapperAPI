from aiohttp import web

from . import get_app

if __name__ == '__main__':
    app = get_app()
    web.run_app(app)
