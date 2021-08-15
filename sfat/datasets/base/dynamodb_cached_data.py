from abc import ABCMeta, abstractmethod
import os
import json
from typing import Dict, List

import pandas as pd

from ...storage import S3
from ...utils.logger import Logger


class DynamoDBCachedData(metaclass=ABCMeta):

    TAG = 'DynamoDBCachedData'
    _cache = {}

    def json(self, force_update: bool = False) -> Dict:
        return self._data(force_update)

    def _data(self, force_update: bool = False):

        local_cache_path = self._local_cache_path()

        # If the data is already on the memory, use it.
        if local_cache_path in DynamoDBCachedData._cache and not force_update:
            return DynamoDBCachedData._cache[local_cache_path]

        # If cache file already exists, use it.
        if os.path.exists(local_cache_path) and not force_update:
            Logger.i(DynamoDBCachedData.TAG, f'Local cache file {local_cache_path} found, using cached file.')
            DynamoDBCachedData._cache[local_cache_path] = self._load_local_file(local_cache_path)
            return DynamoDBCachedData._cache[local_cache_path]

        # Fetch data from DynamoDB and save to local storage as a file.
        json_data = self._fetch_from_dynamodb()
        Logger.i(DynamoDBCachedData.TAG, f'Fetching data from DynamoDB to {local_cache_path}')
        self._save_local_file(json_data, local_cache_path)
        DynamoDBCachedData._cache[local_cache_path] = json_data
        return DynamoDBCachedData._cache[local_cache_path]

    def df(self, force_update: bool = False) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _local_cache_path(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def _fetch_from_dynamodb(self) -> List[Dict]:
        raise NotImplementedError

    @abstractmethod
    def _load_local_file(self, local_cache_filepath: str) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def _save_local_file(self, json_data: Dict, local_cache_filepath: str) -> None:
        raise NotImplementedError
