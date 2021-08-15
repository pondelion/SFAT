import os
from datetime import datetime, date
from typing import Dict, List

from overrides import overrides
import pandas as pd

from .base.dynamodb_json_cached_data import DynamoDBJsonCachedData
from ..db import DynamoDB
from ..config import DataLocationConfig, AWSConfig


class CompanyAnnouncement(DynamoDBJsonCachedData):

    _dynamo_db = DynamoDB(table_name=AWSConfig.DYNAMODB_COMPANY_ANNOUNCEMENT_TABLE_NAME)

    def __init__(
        self,
        code: int = None,
    ):
        self._code = code

    @overrides
    def _local_cache_path(self) -> str:
        local_cache_path = os.path.join(
            DataLocationConfig.LOCAL_CACHE_DIR,
            'company_announcement',
            f'{self._code}.json',
        )
        return local_cache_path

    @overrides
    def _fetch_from_dynamodb(self) -> List[Dict]:
        res = CompanyAnnouncement._dynamo_db.partitionkey_query(
            partition_key_name='company_code',
            partition_key=int(f'{self._code}0'),
        )
        return res

    @overrides
    def df(self, force_update: bool = False) -> pd.DataFrame:
        jsons = self.json(force_update)
        keys = [
            'company_name',
            'company_code',
            'pubdate',
            'title',
            'markets_string',
            'document_url',
            'url_xbrl',
            'url_report_type_summary',
            'update_history',
            'url_report_type_earnings_forecast',
            'id',
        ]
        # df = pd.DataFrame({
        #     key: [d[key] for d in jsons]
        # } for key in keys)
        df = pd.DataFrame(jsons)
        if len(df) == 0:
            return df
        df['pubdate'] = pd.to_datetime(df['pubdate'])
        df.sort_values(by='pubdate', inplace=True)
        return df[keys]
