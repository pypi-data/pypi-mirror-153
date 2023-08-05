import logging  # noqa
from . import mylogger
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63,gzip(gfe)',
}


def logger(module_name: str, loglevel=None):
    module_logger = mylogger.get_logger(module_name, loglevel=loglevel)
    return module_logger
