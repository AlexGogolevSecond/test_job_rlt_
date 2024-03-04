import asyncio
import json
import datetime
from datetime import datetime
from typing import Optional
import motor.motor_asyncio
from dateutil.parser import parse
from repository import MongoRepository
import sys


client = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)

async def main(data: dict):
    if not isinstance(data, dict):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as ex:
            return 'не удалось преобразовать данные'

    dt_from_str = data.get('dt_from')
    dt_from = parse(dt_from_str)
    dt_upto_str =  data.get('dt_upto')
    dt_upto = parse(dt_upto_str)
    group_type = data.get('group_type')
    if group_type not in ('hour', 'day', 'month'):
        return ''
    group_type = 'dayOfYear' if group_type == 'day' else group_type

    aggregates = await MongoRepository.aggregate(dt_from=dt_from,
                                                 dt_upto=dt_upto,
                                                 group_type=group_type,
                                                 client=client)

    # нужно как-то причесать ответ к требуемому формату:
    '''
    {"dataset": [5906586, 5515874, 5889803, 6092634], "labels":
    ["2022-09-01T00:00:00", "2022-10-01T00:00:00",
    "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
    '''
    dataset = [x.get('total') for x in aggregates]
    labels = [x.get('date') for x in aggregates] 

    result = {'dataset': dataset, 'labels': labels}
    print(result)
    return result


if __name__ == '__main__':
    asyncio.run(main('{"dt_from":"2022-09-01T00:00:00", "dt_upto":"2022-12-31T23:59:00", "group_type":"month"}'))