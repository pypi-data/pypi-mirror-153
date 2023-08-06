
from typing import Dict

from wintersweet.utils.base import Utils
from wintersweet.utils.metaclass import SafeSingleton

from elasticsearch import AsyncElasticsearch


class ElasticsearchManager(SafeSingleton):

    def __init__(self):

        self._config = {}
        self._es_map = {}
        self._ready = False

    @property
    def ready(self):
        return self._ready

    async def initialize(self):

        await self

    def register(self, config: Dict[str, Dict]):
        assert not self.ready, f'{self.__class__.__name__} already registered'
        self._config = config

    def __await__(self):
        if self._ready:
            return self

        for es_name, conf in self._config.items():

            es_client = AsyncElasticsearch(**conf)

            result = yield from es_client.ping()
            if result is False:
                raise Exception(f'"{es_name}" ping failed !')
            else:
                Utils.log.success(f'Elasticsearch [{es_name}] hosts:{es_client.transport.hosts} initialized')

            self._es_map[es_name] = es_client

        self._ready = True

    def get_client(self, es_name='default'):
        assert es_name in self._es_map, f'es_name: "{es_name}" not found'
        return self._es_map[es_name]


es_manager = ElasticsearchManager()

