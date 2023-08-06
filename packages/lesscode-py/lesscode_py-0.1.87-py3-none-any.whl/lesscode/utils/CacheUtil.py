import copy
import datetime
import functools
import json
import logging
import traceback

from lesscode.db.redis.redis_helper import RedisHelper
from tornado.options import options

# 装饰器
from util.JsonUtil import JSONEncoder


def Cache(ex=3600 * 8, cache_key=None):
    def cache_func(func):
        # 默认key生成方法：str(item)
        @functools.wraps(func)
        def cache_wrapper(*args, **params):
            return deal_cache(func, ex, cache_key, *args, **params)

        return cache_wrapper

    return cache_func


def deal_cache(func, ex, cache_key, *args, **params):
    # 获取缓存查询key
    params = dict(sorted(params.items(), key=lambda x: x[0]))
    func_name = str(func).split(" ")[1]
    if not cache_key:
        cache_key = format_insert_key(func_name, params)
    value = query_cache(cache_key)
    if value:
        data = value
    else:
        start = datetime.datetime.now()
        logging.info("[组件：{}]数据开始计算！".format(func_name))
        copy_params = copy.deepcopy(params)
        data = func(*args, **copy_params)

        # 插入缓存表
        insert_cache(data, ex, cache_key)
        logging.info("[组件：{}]数据缓存已刷新！用时{}".format(func_name, datetime.datetime.now() - start))

    return data


def query_cache(cache_key):
    if options.cache_module:
        data = RedisHelper("redis_con_1").sync_get(cache_key)
        if data:
            value = json.loads(data)
            return value
        else:
            logging.info("str_select_key为".format(cache_key))
            return False
    return False


def format_insert_key(func_name, params):
    str_insert_key = ""
    for k in params:
        if isinstance(params[k], dict):
            a = json.dumps(params[k])
        else:
            a = str("" if params[k] is None else params[k])

        str_insert_key = str_insert_key + a + "&"
    str_insert_key = str_insert_key[:-1]
    str_insert_key = func_name + "_" + str_insert_key

    return str_insert_key


def insert_cache(data, ex, cache_key):
    if options.cache_module:
        try:
            RedisHelper("redis_con_1").sync_set(cache_key, JSONEncoder().encode(data), ex=ex)
        except:
            logging.error(traceback.format_exc())
