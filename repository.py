class MongoRepository():
    """Репозиторий для монго"""
    @classmethod
    def add(cls, **filter):
        pass

    @classmethod
    def get(cls, **filter):
        pass

    @classmethod
    async def aggregate(cls, **filter):
        """Получаем агрегированные данные"""

        dt_from = filter.get('dt_from')
        dt_upto = filter.get('dt_upto')
        group_type = filter.get('group_type')
        client = filter.get('client')

        if not all([dt_from, dt_upto, group_type, client is not None]):
            return None

        pipeline = [
            {
                '$match': {
                    'dt': {
                        '$gte': dt_from, 
                        '$lte': dt_upto
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        f'{group_type}': {
                            f'${group_type}': '$dt'
                        }
                    },
                    'total': {
                        '$sum': '$value'
                    },
                    'date': {
                        '$min': '$dt'
                    }
                }
            },
            {
                '$sort': {
                    f'_id.{group_type}': 1
                }
            }
        ]

        res = []
        async with await client.start_session() as s:
            async with s.start_transaction():
                collection = client.testrlt.sample_collection

                async for doc in collection.aggregate(pipeline):
                    print(doc)
                    res.append(doc)

        # aggr = await collection.aggregate(

        # )

        # res = []
        # for v in aggr:
        #     res.append(v)
        #     # print(v)

        return res
