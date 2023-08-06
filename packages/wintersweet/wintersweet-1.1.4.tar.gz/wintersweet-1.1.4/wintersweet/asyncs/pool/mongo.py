
import bson
import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from wintersweet.asyncs.pool.base import BasePoolManager
from wintersweet.utils.base import Utils
from wintersweet.utils.metaclass import SafeSingleton


class MongoPool(AsyncIOMotorClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = None

    @property
    def name(self):
        return self._name

    async def health(self):
        result = False

        try:
            result = bool(await self.server_info())
        except Exception as err:
            Utils.log.error(err)

        return result


class MongoPoolManager(SafeSingleton, BasePoolManager):
    """mongo池化管理器"""
    def __init__(self):
        super(MongoPoolManager, self).__init__()

    def __await__(self):
        if self._ready:
            return self

        for pool_name, pool_config in self._config.items():
            yield
            self._pools[pool_name] = MongoPool(**pool_config)
            setattr(self._pools[pool_name], '_name', pool_name)
            Utils.log.success(
                f"mongo pool {self.pool_status(pool_name)} initialized"
            )

        self._ready = True

    def pool_status(self, pool_name='default'):
        pool = self._pools[pool_name]

        return f'<[{pool_name}] {pool.address} [size:[{pool.min_pool_size}:{pool.max_pool_size}]]>'

    def _echo_pool_info(self, pool_name='default'):
        pool = self._pools[pool_name]
        for address, server in pool.delegate._topology._servers.items():

            pool_size = len(server.pool.sockets) + server.pool.active_sockets

            if (pool.max_pool_size - pool_size) < Utils.math.ceil(pool.max_pool_size / 3):
                Utils.log.warning(
                    f'Mongo connection pool not enough ({pool_name}){address}: '
                    f'{pool_size}/{pool.max_pool_size}'
                )

    def get_client(self, pool_name='default'):
        assert pool_name in self._pools, f'pool_name: "{pool_name}" not found'
        self._echo_pool_info(pool_name)
        pool = self._pools[pool_name]
        return pool

    def get_collection(self, db_name, collection_name, pool_name='default'):
        """获取指定集合，无须集合存在，操作时将自动创建集合"""
        return self.get_client(pool_name)[db_name][collection_name]

    def get_collection_by_date(self, db_name, collection_name, date: datetime.date = None, pool_name='default'):
        """按日期切分集合，无须集合存在，操作时将自动创建集合"""
        if not date:
            date = datetime.datetime.now()
        date_str = Utils.datetime2time(date, format_type='%Y%m%d')
        return self.get_client(pool_name)[db_name][f'{collection_name}_{date_str}']

    def get_collection_by_month(self, db_name, collection_name, date: datetime.date = None, pool_name='default'):
        """按月切分集合，无须集合存在，操作时将自动创建集合"""
        if not date:
            date = datetime.datetime.now()
        month_str = Utils.datetime2time(date, format_type='%Y%m')
        return self.get_client(pool_name)[db_name][f'{collection_name}_{month_str}']

    @staticmethod
    def convert_mongo_id(mongo_id):
        """转换字符串mongo id为bson ObjectId"""
        try:
            return bson.ObjectId(mongo_id)
        except bson.errors.InvalidId:
            return bson.ObjectId()

    def close(self):
        _pools, self._pools = self._pools, {}
        for pool in _pools:
            pool.close()


mongo_pool_manager = MongoPoolManager()
