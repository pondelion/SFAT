from abc import ABCMeta, abstractmethod
import json
import os
from typing import Dict
from decimal import Decimal

from overrides import overrides

from .dynamodb_cached_data import DynamoDBCachedData


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class DynamoDBJsonCachedData(DynamoDBCachedData, metaclass=ABCMeta):

    @overrides
    def _load_local_file(self, local_cache_filepath: str) -> Dict:
        with open(local_cache_filepath, 'r') as f:
            json_data = json.load(f)
        return json_data

    @overrides
    def _save_local_file(self, json_data: Dict, local_cache_filepath: str) -> None:
        os.makedirs(os.path.dirname(local_cache_filepath), exist_ok=True)
        json_str = json.dumps(json_data, default=decimal_default)
        with open(local_cache_filepath, 'w') as f:
            f.write(json_str)
