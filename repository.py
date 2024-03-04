""""""
# import abc


# class AbstractRepository(abc.ABC):
#     model = None

#     @abc.abstractmethod
#     def get(self, **filter):
#         raise NotImplementedError

#     @abc.abstractmethod
#     def add(self, **filter):
#         raise NotImplementedError


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

        return None
