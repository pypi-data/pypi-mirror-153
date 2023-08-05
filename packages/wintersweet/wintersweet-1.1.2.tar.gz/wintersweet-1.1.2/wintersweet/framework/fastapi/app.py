import copy
import logging

from fastapi import FastAPI

from wintersweet import project_label
from wintersweet.utils.logging import register_logger
from wintersweet.framework.conf import settings
from wintersweet.asyncs.pool.mysql import mysql_pool_manager
from wintersweet.asyncs.pool.redis import redis_pool_manager
from wintersweet.asyncs.pool.es import es_manager

DEFAULT_HEADERS = [(r'Server', project_label)]


def create_app():
    settings.initialize()
    app_config = copy.deepcopy(settings.APP_CONFIG)
    on_startup = app_config.get('on_startup', [])
    assert isinstance(on_startup, (list, tuple)), 'on_startup must be list or tuple'
    _on_startup = [*on_startup]
    app_config['on_startup'] = _on_startup
    if settings.DATABASES:
        mysql_pool_manager.register(settings.DATABASES)
        _on_startup.insert(0, mysql_pool_manager.initialize)

    if settings.REDIS_CONFIG:
        redis_pool_manager.register(settings.REDIS_CONFIG)
        _on_startup.insert(0, redis_pool_manager.initialize)

    if settings.ES_CONFIG:
        es_manager.register(settings.ES_CONFIG)
        _on_startup.insert(0, es_manager.initialize)

    app = FastAPI(**app_config)
    logging.getLogger(r'fastapi').setLevel(settings.LOGGING_CONFIG['level'].upper())

    register_logger(
        **settings.LOGGING_CONFIG,
        debug=settings.DEBUG
    )
    for middleware in settings.MIDDLEWARES:
        app.add_middleware(middleware['cls'], **middleware['options'])

    for exception_handler in settings.EXCEPTION_HANDLERS:
        app.add_exception_handler(exception_handler['cls'], exception_handler['handler'])

    return app
