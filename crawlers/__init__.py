# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/23 20:15

@desc:

'''

from base.realestate import RealEstate

from base import errors
from base.errors import BaseError
from base.errors import NetworkError
from base.errors import DDoSProtection
from base.errors import RequestError
from base.errors import RequestTimeout

from crawlers.tongcheng58 import tongcheng58
from crawlers.anjuke import anjuke
from crawlers.leyoujia import leyoujia
from crawlers.fang import fang

realEstate = [
    'tongcheng58',
    'anjuke',
    'leyoujia',
]

base = [
    'RealEstate',
    'realEstate'
]

__all__ = base + errors.__all__ + realEstate
