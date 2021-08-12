import os
from datetime import datetime, date

from overrides import overrides
import pandas as pd

from .base.s3_csv_cached_data import S3CSVCachedData
from ..config import DataLocationConfig


class CompanyFinancials(S3CSVCachedData):

    @overrides
    def _local_cache_path(self) -> str:
        local_cache_path = os.path.join(
            DataLocationConfig.LOCAL_CACHE_DIR,
            'company_financials.csv'
        )
        return local_cache_path

    @overrides
    def _source_path(self) -> str:
        source_path = DataLocationConfig.COMPANY_DATA
        return source_path
