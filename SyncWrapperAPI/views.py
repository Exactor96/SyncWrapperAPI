import asyncio
import os
from json.decoder import JSONDecodeError

from aiohttp import web, ClientSession
from aiohttp.web_response import Response
from aiohttp.web_request import Request

from .config import (PROXY_URLS, ASYNC_PROXY_URLS, ASYNC_PROCESSING_URL, WAITING_BETWEEN_REQUESTS,
                     ASYNC_TIMEOUT, USER_AGENT_ADD)


async def _fetch(session: ClientSession, request: Request, api_key: str) -> dict:
    """Синхронный запрос к сервису."""
    redirect_url = PROXY_URLS.get(request.path) or ASYNC_PROXY_URLS.get(request.path)
    if not redirect_url:
        return {'message': 'url not found'}
    try:
        json = await request.json()
    except JSONDecodeError as error:
        return {'error': 'invalid json format', 'message': error.msg}
    async with session.post(redirect_url, headers={'apikey': api_key}, json=json) as response:
        return await response.json()


async def _async_fetch(session: ClientSession, request: Request, api_key: str, json: dict) -> dict:
    """Асинхронный запрос к сервису с поддержкой long polling."""
    redirect_url = ASYNC_PROXY_URLS.get(request.path)
    if not redirect_url:
        return {'message': 'url not found'}
    r = await session.post(redirect_url, headers={'apikey': api_key}, json=json)
    json = await r.json()
    task_id = json.get('id')
    result_url = os.path.join(ASYNC_PROCESSING_URL, task_id)
    for i in range(0, ASYNC_TIMEOUT, WAITING_BETWEEN_REQUESTS):
        r = await session.get(
            result_url,
            headers={'apikey': api_key, 'User-Agent': ' '.join([request.headers['User-Agent'], USER_AGENT_ADD])},
        )
        result = await r.json()
        if result['done'] is True:
            response = result['response'][0]  # Всегда возвращает список
            response.update({'op_id': task_id})
            return response
        await asyncio.sleep(WAITING_BETWEEN_REQUESTS)
    return {'message': f'{ASYNC_TIMEOUT}s timeout reached'}


async def sync_proxy(request: Request) -> Response:
    """Обработчик для синхронных запросов."""
    api_key = request.headers.get('apikey')
    if api_key:
        async with ClientSession() as session:
            response_json = await _fetch(session, request, api_key)
    else:
        response_json = {'error': 'no api key in headers'}
    return web.json_response(response_json)


async def async_proxy(request: Request) -> Response:
    """Обработчик для синхронных/асинхронных запросов."""
    api_key = request.headers.get('apikey')
    if api_key:
        try:
            json = await request.json()
        except JSONDecodeError as error:
            web.json_response({'error': 'invalid json format', 'message': error.msg})
        else:
            async with ClientSession() as session:
                if json['service'].get('async') is True:
                    response_json = await _async_fetch(session, request, api_key, json)
                else:
                    response_json = await _fetch(session, request, api_key)
    else:
        response_json = {'error': 'no api key in headers'}
    return web.json_response(response_json)
