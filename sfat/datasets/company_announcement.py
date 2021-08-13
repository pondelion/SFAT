import os
from datetime import datetime, date

from overrides import overrides
import pandas as pd

from .base.s3_csv_cached_data import S3CSVCachedData
from ..config import DataLocationConfig


class CompanyAnnouncement():

    def __init__(
        self,
        code: int = None,
    ):
        self._code = code
