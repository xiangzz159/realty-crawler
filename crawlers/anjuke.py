# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/23 19:08

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup
import requests
import config
from fontTools.ttLib import TTFont
from io import BytesIO
import base64
import re
import matplotlib

class anjuke(RealEstate):
    new_house_url = 'https://%s.fang.anjuke.com/'
    second_hand_url = 'https://%s.anjuke.com/sale/'
    rental_url = 'https://%s.zu.anjuke.com/'

    # 新房信息
    def get_new_hourse_infos(self, city):
        url = self.new_house_url % city
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('div.key-list > div.item-mod')
        infos = []
        for i in items[:1]:
            link = i.get('data-link')
            infos.append(self.get_new_house_info(link))
        return infos

    def get_new_house_info(self, link):
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title = soup.select('div.basic-info > h1')
            title = title[0].text.strip().replace('\n', '').replace(' ', '')
            base_params = soup.select('dl.basic-parms > dd')
            price = base_params[0].text.strip().replace('\n', '').replace(' ', '').replace('\uebf4变价通知我', '')
            open_time = base_params[1].text.strip().replace('\n', '').replace(' ', '').replace('\uebf3开盘通知我', '')
            completion_time = base_params[2].text.strip().replace('\n', '').replace(' ', '')
            house_type = base_params[3].text.strip().replace('\n', '').replace(' ', '').replace('\uebf2全部户', '')
            address = base_params[4].text.strip().replace('\n', '').replace(' ', '').replace('\uebf5查看地图', '')
            detail = soup.select('div.louping-detail')[0].text.strip().replace('\n', '').replace(' ', '')
            return {
                'title': title,
                'price': price,
                'open_time': open_time,
                'completion_time': completion_time,
                'house_type': house_type,
                'address': address,
                'detail': detail,
                'link': link
            }

        except Exception as e:
            print('数据抓取失败：%s, url:%s' % (str(e), link))



    # 二手房信息
    def get_second_hand_infos(self, city):
        pass

    # 租房信息
    def get_rental_infos(self, city):
        pass


f = anjuke()
f.get_new_hourse_infos('sz')