#！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/31 10:33

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup


class ke(RealEstate):
    def describe(self):
        return self.deep_extend(super(ke, self).describe(), {
            'id': 'ke',
            'name': '贝壳',
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
        if self.has['fetchNewHouse'] == False:
            return None
        url = self.urls['new_house_url'] % city

    def analysis_new_house_page(self, link):
        if self.has['fetchNewHouse'] == False:
            return None
        pass

    def fetch_rental_links(self, city):
        if self.has['fetchRentalLinks'] == False:
            return None
        pass

    def analysis_rental_page(self, link):
        if self.has['fetchRentalLinks'] == False:
            return None
        pass

    def fetch_second_hand_links(self, city):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        pass

    def analysis_second_hand_page(self, link):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        pass
