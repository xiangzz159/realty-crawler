# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2018/9/17 20:27

@desc: config

'''

# 数据库
DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = ''
DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + str(
    DB_PORT) + '/' + DB_NAME + '?charset=utf8'

# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''

# MongoDB
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
