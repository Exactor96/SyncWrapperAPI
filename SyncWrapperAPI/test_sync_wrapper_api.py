import os

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from . import get_app
from SyncWrapperAPI.config import PROXY_URLS, ASYNC_PROXY_URLS


class SyncWrapperAPITestCase(AioHTTPTestCase):
    """Проверка синхронных и асинхронных запросов через proxy."""
    api_key = os.getenv('test_api_key')
    sync_fixtures = {
        '/ai/text/translate': {
            "context": {
                "text": "A sample text",
                "to": "es"
            },
            "service": {
                "provider": "ai.text.translate.microsoft.translator_text_api.3-0"
            }
        },

        '/ai/text/detect-language': {
            "context": {
                "text": "Hello, I would like to take a class at your University.",
            },
            "service": {
                "provider": "ai.text.detect-language.microsoft.text_analytics_api.2-1"
            }
        },

        '/ai/text/sentiment': {
            "context": {
                "text": "We love this trail and make the trip every year."
                        " The views are breathtaking and well worth the hike!",
                "lang": "en"
            },
            "service": {
                "provider": "ai.text.sentiment.meaningcloud.sentiment_analysis_api.2-1"
            }
        },

        '/ai/text/dictionary': {
            "context": {
                "text": "kick",
                "from": "en",
                "to": "ru"
            },
            "service": {
                "provider": "ai.text.dictionary.yandex.dictionary_api.1-0"
            }
        },

        '/ai/text/classify': {
            "context": {
                "text": "...",
                "lang": "en"
            },
            "service": {
                "provider": "ai.text.classify.ibm.natural_language_understanding"
            }
        },

        '/ai/text/transliterate': {
            "context": {
                "text": "こんにちは",
                "language": "ja",
                "fromscript": "jpan",
                "toscript": "latn"
            },
            "service": {
                "provider": "ai.text.transliterate.microsoft.translator_text_api.3-0"
            }
        },

        '/ai/image/tagging': {
            "context": {
                "image": "..."
            },
            "service": {
                "provider": "ai.image.tagging.amazon.recognition_detect_labels_api"
            }
        },
        '/ai/image/ocr': {
            "context": {
                "image": "..."
            },
            "service": {
                "provider": "ai.image.ocr.abbyy.cloud_ocr"
            }
        },
        '/ai/speech/transcribe': {
            "context": {
                "source": "...",
                "language": "en"
            },
            "service": {
                "provider": "ai.speech.transcribe.alibaba.asr_api"
            }
        },

    }

    async_fixtures = {
        '/ai/text/translate': {
            "context": {
                "text": "A sample text",
                "to": "es"
            },
            "service": {
                "provider": "ai.text.translate.microsoft.translator_text_api.3-0",
                "async": True,
            }
        },
    }

    async def get_application(self):
        app = get_app()
        return app

    @unittest_run_loop
    async def test_not_existed_url(self):
        """Проверяет незарегистрированный url."""
        resp = await self.client.request("POST", "/not-existed-url")
        self.assertEqual(404, resp.status)

    @unittest_run_loop
    async def test_not_allowed_method(self):
        """Проверяет недопустимый метод."""
        resp = await self.client.request("DELETE", [k for k in PROXY_URLS.keys()][0])
        self.assertEqual(405, resp.status)

    @unittest_run_loop
    async def test_sync_request(self):
        """Проверяет все зарегистрированные url в режиме "async: false"."""
        url_list = [url for url in PROXY_URLS]
        async_url_list = [url for url in ASYNC_PROXY_URLS]

        for url in url_list + async_url_list:
            json = self.sync_fixtures.get(url)
            resp = await self.client.request("POST", url, headers={'apikey': self.api_key}, json=json)
            self.assertEqual(200, resp.status)

    @unittest_run_loop
    async def test_async_requests(self):
        """Проверка идентичности синхронного и асинхронного запроса."""
        async_url_list = [url for url in ASYNC_PROXY_URLS]

        for url in async_url_list:
            json = self.sync_fixtures.get(url)
            resp = await self.client.request("POST", url, headers={'apikey': self.api_key}, json=json)
            self.assertEqual(200, resp.status)

            json = self.async_fixtures.get(url)
            async_resp = await self.client.request("POST", url, headers={'apikey': self.api_key}, json=json)
            self.assertEqual(200, async_resp.status)
            sync_json = await resp.json()
            async_json = await async_resp.json()
            self.assertEqual(sync_json['results'], async_json['results'],
                             'результаты синхронного и асинхорнного запроса должны совпадать')
