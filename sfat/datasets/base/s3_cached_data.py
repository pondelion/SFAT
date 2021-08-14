from abc import ABCMeta, abstractmethod
import os

import pandas as pd

from ...storage import S3
from ...utils.logger import Logger


class S3CachedData(metaclass=ABCMeta):

    TAG = 'S3CachedData'
    _cache = {}

    # @property
    def df(self, force_update: bool = False) -> pd.DataFrame:
        return self._data(force_update)

    def _data(self, force_update: bool = False):

        local_cache_path = self._local_cache_path()

        # If the data is already on the memory, use it.
        if local_cache_path in S3CachedData._cache and not force_update:
            return S3CachedData._cache[local_cache_path]

        # If cache file already exists, use it.
        if os.path.exists(local_cache_path) and not force_update:
            Logger.i(S3CachedData.TAG, f'Local cache file {local_cache_path} found, using cached file.')
            S3CachedData._cache[local_cache_path] = self._load_local_file(local_cache_path)
            return S3CachedData._cache[local_cache_path]

        # Download csv file from S3.
        source_path = self._source_path()
        self._download_s3_file(
            local_cache_path,
            source_path,
        )
        S3CachedData._cache[local_cache_path] = self._load_local_file(local_cache_path)
        return S3CachedData._cache[local_cache_path]

    @abstractmethod
    def _local_cache_path(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _source_path(self) -> str:
        raise NotImplementedError

    def _download_s3_file(
        self,
        local_dest_path: str,
        source_path: str
    ) -> None:
        os.makedirs(os.path.dirname(local_dest_path), exist_ok=True)
        Logger.i(S3CachedData.TAG, f'Downloading {source_path} to {local_dest_path}')
        S3.download_file(source_path, local_dest_path)

    @abstractmethod
    def _load_local_file(self, local_cache_filepath: str):
        raise NotImplementedError
