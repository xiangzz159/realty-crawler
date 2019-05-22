#！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/10 21:18

@desc: https://cloud.tencent.com/developer/article/1151814

'''

import config
import pymongo
from bson.objectid import ObjectId


class MongoClient(object):

    def __init__(self, db, collection):
        self.client = pymongo.MongoClient(host=config.MONGO_HOST, port=config.MONGO_PORT)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def insert_one(self, obj):
        result = self.collection.insert_one(obj)
        return result

    def insert_many(self, lists):
        results =  self.collection.insert_many(lists)
        return results

    def find_one(self, condition, id=None):
        result = self.collection.find_one({'_id':ObjectId(id)}) if id else self.collection.find_one(condition)
        return result

    def find(self, conditions):
        results = self.collection.find(conditions)
        return results

    def update(self, condition, new_obj):
        result = self.collection.update(condition, new_obj)
        return result

    def remove(self, condition):
        result = self.collection.remove(condition)
        return result
