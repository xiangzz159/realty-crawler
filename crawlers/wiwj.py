# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/31 10:31

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup


class wiwj(RealEstate):
    def describe(self):
        return self.deep_extend(super(wiwj, self).describe(), {
            'id': 'wiwj',
            'name': '我爱我家',
            'spelling': False,  # True为全拼，False为缩写
            'has': {
                'fetchNewHouse': False,
                'fetchSecondHandHouse': True,
                'fetchRentalLinks': True
            },
            'urls': {
                'new_house_url': '',
                'second_hand_url': '',
                'rental_url': ''
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
