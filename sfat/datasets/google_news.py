import os
from datetime import datetime, date
from typing import Dict, List
import re
from dateutil import parser
from pytz import timezone

from overrides import overrides
import pandas as pd

from .base.dynamodb_json_cached_data import DynamoDBJsonCachedData
from ..db import DynamoDB
from ..config import DataLocationConfig, AWSConfig


class GoogleNews(DynamoDBJsonCachedData):

    _dynamo_db = DynamoDB(table_name=AWSConfig.DYNAMODB_GOOGLE_RSS_NEWS_TABLE_NAME)

    def __init__(
        self,
        publised_date: date,
    ):
        self._pub_date = publised_date

    @overrides
    def _local_cache_path(self) -> str:
        local_cache_path = os.path.join(
            DataLocationConfig.LOCAL_CACHE_DIR,
            'google_news',
            f'{self._pub_date.strftime("%Y%m%d")}.json',
        )
        return local_cache_path

    @overrides
    def _fetch_from_dynamodb(self) -> List[Dict]:
        res = GoogleNews._dynamo_db.partitionkey_query(
            partition_key_name='published_date',
            partition_key=self._pub_date.strftime('%Y-%m-%d'),
        )
        return res

    @overrides
    def df(self, force_update: bool = False) -> pd.DataFrame:
        news_jsons = self.json(force_update)
        reg_obj = re.compile(r"<[^>]*?>")
        summaries = [reg_obj.sub('', r['summary']).replace('&nbsp;', ' ') for r in news_jsons]
        titles = [reg_obj.sub('', r['title']).replace('&nbsp;', ' ') for r in news_jsons]
        published_list = [parser.parse(r['published']).astimezone(timezone('Asia/Tokyo')) for r in news_jsons]
        published_list_gmt = [parser.parse(r['published']) for r in news_jsons]
        topics = [r['topic'] for r in news_jsons]
        #published_date_list =  [r['published_date'] for r in news_jsons]
        published_date_list =  [pub.strftime('%Y-%m-%d') for pub in published_list]
        df = pd.DataFrame({
            'published': published_list,
            'published_gmt': published_list_gmt,
            'published_date': published_date_list,
            'title': titles,
            'summary': summaries,
            'topic': topics
        })
        return df
