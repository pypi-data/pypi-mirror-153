
DEBUG = True
SECRET = f'__access_control_{DEBUG}_@5806fecc-93b3-11ec-beda-e2b55ff3da64__'

LISTEN_PORT = 8080

# process
PROCESS_NUM = 2


APP_CONFIG = {
    'debug': DEBUG,
    'routes': [],
}


LOGGING_CONFIG = {
    'level': 'debug',
    'file_path': '',
    'file_rotation': None,
    'file_retention': None,
}

# MIDDLEWARES
MIDDLEWARES = [

]

EXCEPTION_HANDLERS = [
    # {
    #     'cls': HTTPException,
    #     'handler': http_exception_handler
    # },
]

DATABASES = {
    # 'default': {
    #     'echo': True,
    #     'host': "localhost",
    #     'user': 'root',
    #     'password': "",
    #     'db': 'test',
    #     'port': 3306,
    #     'charset': r'utf8',
    #     'autocommit': True,
    #     'cursorclass': aiomysql.DictCursor,
    # }
}

REDIS_CONFIG = {
    # 'default': {
    #     'address': "redis://localhost:6379",
    #     'password': None,
    #     'db': 0,
    #     'encoding': 'utf-8',
    #     'minsize': 10
    # }
}

ES_CONFIG = {

}
