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


def update_date(date: datetime, group_type: str) -> Optional[str]:
    """Приводим дату/время к требуемому формату_summary_

    Args:
        date (datetime): дата/время
        group_type (str): тип агрегации

    Returns:
        str: результурующая строка даты/времени в формате ISO
    """
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour

    result = None

    if group_type == 'month':
        result = datetime(year=year, month=month, day=1)
    elif group_type == 'dayOfYear':
        result = datetime(year=year, month=month, day=day)
    elif group_type == 'hour':
        result = datetime(year=year, month=month, day=day, hour=hour)

    return result.strftime('%Y-%m-%dT%H:%M:%S')


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

    dataset = [x.get('total') for x in aggregates]
    labels = [update_date(x.get('date'), group_type) for x in aggregates]

    return {'dataset': dataset, 'labels': labels}


if __name__ == '__main__':
    asyncio.run(main('{"dt_from":"2022-09-01T00:00:00", "dt_upto":"2022-12-31T23:59:00", "group_type":"month"}'))