# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/31 9:58

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup


class sofang(RealEstate):
    def describe(self):
        return self.deep_extend(super(sofang, self).describe(), {
            'id': 'sofang',
            'name': '搜房网',
            'spelling': False,  # True为全拼，False为缩写
            'has': {
                'fetchNewHouse': False,
                'fetchSecondHandHouse': True,
                'fetchRentalLinks': True
            },
            'urls': {
                'new_house_url': '',
                'second_hand_url': 'http://%s.sofang.com/esfsale/area',
                'rental_url': 'http://%s.sofang.com/esfrent/area'
            }
        })

    def fetch_new_hourse_links(self, city):
        pass

    def analysis_new_house_page(self, link):
        pass

    def fetch_rental_links(self, city):
        pass

    def analysis_rental_page(self, link):
        pass

    def fetch_second_hand_links(self, city):
        pass

    def analysis_second_hand_page(self, link):
        pass

