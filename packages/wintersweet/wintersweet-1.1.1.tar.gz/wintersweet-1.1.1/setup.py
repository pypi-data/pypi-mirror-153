# -*- coding: utf-8 -*-

import setuptools

from wintersweet import __version__


with open(r'README.md', r'r', encoding=r'utf8') as stream:
    long_description = stream.read()

setuptools.setup(
    name=r'wintersweet',
    version=__version__,
    license=r'Apache License Version 2.0',
    platforms=[r'all'],
    author=r'Xixi.Dong',
    author_email=r'xq1889@163.com',
    description=r'Network Development Suite',
    long_description=long_description,
    long_description_content_type=r'text/markdown',
    url=r'https://gitee.com/xixigroup/wintersweet',
    packages=setuptools.find_packages(),
    python_requires=r'>= 3.8',
    install_requires=[
        r'APScheduler==3.7.0',
        r'Pillow==8.2.0',
        r'PyJWT==2.1.0',
        r'PyYAML==5.4.1',
        r'SQLAlchemy==1.3.24',
        # r'http==3.7.4',
        r'aiomysql==0.0.21',
        r'aioredis==1.3.1',
        r'async-timeout==3.0.1',
        r'cachetools==4.2.2',
        r'cryptography==3.4.7',
        r'fastapi==0.65.1',
        r'gunicorn==20.1.0',
        r'hiredis==2.0.0',
        r'httptools==0.2.0',
        r'loguru==0.5.3',
        r'motor==2.4.0',
        r'ntplib==0.3.4',
        r'numpy==1.20.3',
        r'protobuf==3.17.1',
        r'psutil==5.8.0',
        r'pyahocorasick==1.4.2',
        r'pytest-asyncio==0.15.1',
        r'pytest==6.2.4',
        r'python-multipart==0.0.5',
        r'qrcode==6.1',
        r'ujson==4.0.2',
        r'uvicorn==0.13.4',
        r'uvloop==0.15.3;sys_platform!="win32"',
        r'xmltodict==0.12.0',
        r'aiofiles==0.8.0',
        r'elasticsearch==8.1.2',
    ],
    classifiers=[
        r'Programming Language :: Python :: 3.8',
        r'License :: OSI Approved :: Apache Software License',
        r'Operating System :: POSIX :: Linux',
    ],
    include_package_data=True
)
