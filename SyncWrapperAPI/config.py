import os


PROXY_URLS = {
    '/ai/text/detect-language': 'https://api.inten.to/ai/text/detect-language',
    '/ai/text/sentiment': 'https://api.inten.to/ai/text/sentiment',
    '/ai/text/dictionary': 'https://api.inten.to/ai/text/dictionary',
    '/ai/text/classify': 'https://api.inten.to/ai/text/classify',
    '/ai/text/transliterate': 'https://api.inten.to/ai/text/transliterate',
    '/ai/image/tagging': 'https://api.inten.to/ai/image/tagging',
    '/ai/image/ocr': 'https://api.inten.to/ai/image/ocr',
    '/ai/speech/transcribe': 'https://api.inten.to/ai/speech/transcribe',
}

ASYNC_PROXY_URLS = {
    '/ai/text/translate': 'https://api.inten.to/ai/text/translate',
}

ASYNC_PROCESSING_URL = 'https://api.inten.to/operations/'

ASYNC_TIMEOUT = int(os.getenv('async-timeout', 120))
WAITING_BETWEEN_REQUESTS = int(os.getenv('waiting', 1))
USER_AGENT_ADD = '/SyncWrapperAPI'
