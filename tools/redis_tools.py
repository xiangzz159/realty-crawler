# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2018/10/19 10:01

@desc:
http://www.cnblogs.com/melonjiang/p/5342383.html
http://www.cnblogs.com/melonjiang/p/5342505.html
'''

import redis
import config
import json


class RedisClient(object):

    def __init__(self):
        self.r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    def keys(self):
        result = self.r.keys()
        if result is None:
            return None
        return result

    def get(self, key):
        result = self.r.get(key)
        if result is None:
            return None
        return json.loads(result)

    def set(self, key, val):
        if len(val) == 0:
            return
            self.r.set(key, json.dumps(val))

    def rm(self, key):
        self.r.delete(key)

    # 设置过期时间（秒）
    def setex(self, key, val, time=60):
        if len(val) == 0:
            return
            self.r.setex(key, json.dumps(val), time)

    # 设置过期时间（毫秒）
    def psetex(self, key, val, time=1000):
        if len(val) == 0:
            return
            self.r.psetex(key, time, json.dumps(val))

    # 设置新值并返回旧值
    def getset(self, key, val):
        if len(val) == 0:
            return
        return self.r.getset(key, json.dumps(val))

    # 自增
    def incr(self, key, amount=None):
        if amount is None:
            return self.r.incr(key)
        else:
            return self.r.incr(key, amount=amount)

    # 在key对应的list中添加元素，每个新的元素都添加到列表的最左边
    def rpush(self, key, value):
        self.r.rpush(key, json.dumps(value))

    # 删除列表右侧第一个元素，并返回该值
    def lpop(self, key):
        return json.loads(self.r.lpop(key))

    def lindex(self, key, index=0):
        return json.loads(self.r.lindex(key, index))

    # 返回列表长度
    def llen(self, key):
        return self.r.llen(key)

    # 分片获取元素
    def lrange(self, key, start, end):
        return self.r.lrange(key, start, end)
