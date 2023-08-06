# wintersweet



#### 介绍

 基于fastapi高性能web框架，结合aiohttp、aiomysql、aioredis等常用异步库，整合为一套简单易用的二次封装框架，使用者可以通过简单的demo和配置，即可快速搭建web服务，其中还包含各种易用的工具供开发者使用

#### 软件架构
- asyncs                                    														异步工具库
    - pool																						 池相关
      - base																				 基类
      - context                                                                            上下文管理
      - mysql                                                                               mysql池相关
      - redis                                                                                 redis池相关
      - mongo                                                                             mongo池相关
    - task                                                                                         任务工具库
      - interface                                                                         接口定义
      - tasks                                                                                任务相关
    - tools                                                                                       其他工具
      - circular                                                                           循环器    
- framework                                                                                   框架工具库
    - conf                                                                                       配置文件解析
    - fastapi                                                                                   fastapi主启动工具
    - exception_handlers                                                            全局异常处理器
    - global_setting                                                                      全局配置文件
    - middlewares                                                                        中间件
    - request                                                                                 请求相关工具
    - response                                                                              标准返回定义
- utils
    - base                                                                                      基础工具
    - errors                                                                                   错误定义
    - logging                                                                                 日志模块
    - metaclass                                                                            元类

#### 安装教程

Version: python >=3.8

###### 下载

```bash
git clone git@gitee.com:xixigroup/wintersweet.git
```

###### pip安装

```bash
pip install wintersweet
```



#### 使用说明

- 本项目指在提供一套快速开发工具，使用者仅通过少量的配置即可快速便捷的使用包括框架、数据库、缓存等工具，在尽可能的精简的前提下最大限度满足使用者的开发场景要求。本项目立足于fastapi，集成各异步库，以最大程度降低使用者异步编程学习成本，体会并发编程的乐趣

#### 参与贡献

@xixi.Dong @wsb

#### 特技

##### 基于Redis的分布式锁

```python
# acquire周期内将持续持有锁
async with MutexLock(redis_pool, 'test-key', 60) as lock:
     is_locked = await lock.acquire()
     if is_locked:
          # do something
     else:
          # do something
```





....
