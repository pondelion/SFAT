from abc import ABCMeta, abstractmethod
import os

import pandas as pd
from overrides import overrides

from ...storage import S3
from ...utils.logger import Logger
from .s3_cached_data import S3CachedData


class S3CSVCachedData(S3CachedData, metaclass=ABCMeta):

    @overrides
    def _load_local_file(self, local_cache_filepath: str):
        return pd.read_csv(local_cache_filepath)
