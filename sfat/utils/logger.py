import logging
from datetime import datetime
import os

import yaml


formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(format=formatter)


class Logger:
    logger = logging.getLogger('sfat')
    try:
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..',
            'log',
            f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        )
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file_handler = logging.FileHandler(
            filename=filename
        )
        file_handler.setFormatter(logging.Formatter(formatter))
        logger.addHandler(file_handler)
    except Exception as ex:
        print(ex)

    @staticmethod
    def d(tag: str, message: str):
        """debug log"""
        Logger.logger.setLevel(logging.DEBUG)
        Logger.logger.debug('[%s] %s', tag, message)

    @staticmethod
    def i(tag: str, message: str):
        """infomation log"""
        Logger.logger.setLevel(logging.INFO)
        Logger.logger.info('[%s] %s', tag, message)

    @staticmethod
    def e(tag: str, message: str):
        """error log"""
        Logger.logger.setLevel(logging.ERROR)
        Logger.logger.error('[%s] %s', tag, message)

    @staticmethod
    def w(tag: str, message: str):
        """warning log"""
        Logger.logger.setLevel(logging.WARNING)
        Logger.logger.warn('[%s] %s', tag, message)
