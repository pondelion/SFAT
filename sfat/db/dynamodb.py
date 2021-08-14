from typing import Dict, List, Union

from boto3.dynamodb.conditions import Key

from ..aws.resource import DYNAMO_DB
from ..utils.logger import Logger
from .db import DB, DBType


class DynamoDB(DB):

    def __init__(self, table_name: str):
        self._table_name = table_name
        try:
            self._table = DYNAMO_DB.Table(self._table_name)
        except Exception as e:
            Logger.e('DynamoDB', f'Failed at DYNAMO_DB.Table({self._table}) : {e}')
            raise e

    def save(
        self,
        items: Union[Dict, List[Dict]],
        use_batch_writer: bool = False,
    ) -> List:
        if not isinstance(items, list):
            items = [items]

        responses = []

        if use_batch_writer:
            with self._table.batch_writer() as batch:
                for item in items:
                    try:
                        responses.append(
                            batch.put_item(
                                Item=item,
                            )
                        )
                    except Exception as e:
                        Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB. Skipping : {e}')
        else:
            for item in items:
                try:
                    responses.append(
                        self._table.put_item(
                            TableName=self._table_name,
                            Item=item,
                        )
                    )
                except Exception as e:
                    Logger.e('DynamoDB#put_item', f'Failed to put data to DynamoDB. Skipping : {e}')

        return responses

    def get(
        self,
        key_condition_expression = None,
        filter_expression = None,
        **kwargs,
    ) -> List[Dict]:
        items = []
        if key_condition_expression is not None:
            kwargs.update({'KeyConditionExpression': key_condition_expression})
        if filter_expression is not None:
            kwargs.update({'FilterExpression': filter_expression})
        try:
            response = self._table.query(
                **kwargs,
            )
            items += response['Items']

            while 'LastEvaluatedKey' in response:
                response = self._table.query(
                    **kwargs,
                    ExclusiveStartKey=response['LastEvaluatedKey'],
                )
                items += response['Items']
        except Exception as e:
            Logger.e('DynamoDB#partitionkey_query', f'Failed to query : {e}')
            return []

        return items

    def partitionkey_query(
        self,
        partition_key_name: str,
        partition_key: str,
    ) -> List[Dict]:
        return self.get(
            key_condition_expression=Key(partition_key_name).eq(partition_key),
        )

    def get_list(self) -> List[Dict]:
         # scan
         raise NotImplementedError

    @property
    def type(self):
        return DBType.DYNAMO_DB
