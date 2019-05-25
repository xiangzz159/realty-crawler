# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/22 19:24

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


class tongcheng58(RealEstate):
    new_house_url = ''
    second_hand_url = 'https://%s.58.com/ershoufang/'
    rental_url = 'https://%s.58.com/chuzu/'

    # 新房信息
    def get_new_hourse_infos(self, city):
        # 安居客
        pass

    # 租房信息
    def get_rental_infos(self, city):
        url = self.rental_url % (city)
        wb_datas = self.fetch(url)
        soup = BeautifulSoup(wb_datas, 'lxml')
        items = soup.select('ul.house-list > li > div.des > h2 > a')
        infos = []
        for i in items:
            link = i.get('href')
            if 'e.58.com' in link:
                continue
            if link[:2] == '//':
                link = 'https:' + link

            infos.append(self.get_rental_info(link))
        return infos

    def get_rental_info(self, link):
        try:
            wb_data = self.fetch(link)
            bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", wb_data)[0]
            soup = BeautifulSoup(wb_data, 'lxml')

            title = soup.select('div.house-title > h1')[0].text.strip()
            title = self.show_real_numb(title, bs64_str)

            pay_way = soup.select('div.house-pay-way > span')
            price = pay_way[0].text.strip()
            price = self.show_real_numb(price, bs64_str)
            deposit_way = pay_way[1].text.strip()

            base_desc = soup.select('ul.f14 > li > span')
            lease_way = base_desc[1].text.strip()
            house_type = base_desc[3].text.strip().replace('\n', '').replace(' ', '')
            house_type = self.show_real_numb(house_type, bs64_str)
            toward = base_desc[5].text.strip().replace('\n', '').replace(' ', '')
            toward = self.show_real_numb(toward, bs64_str)
            address1 = base_desc[7].text.strip()
            area = base_desc[9].text.strip().replace('\n', '').replace(' ', '')
            address2 = base_desc[11].text.strip()
            address = area + '_' + address2 + '_' + address1

            introduce_item = soup.select('ul.introduce-item > li')
            bright_spot = introduce_item[0].text.strip().replace('\n', '').replace(' ', '')
            desc = introduce_item[1].text.strip().replace('\n', '').replace(' ', '')
            return {
                'title': title,
                'price': price,
                'deposit_way': deposit_way,
                'lease_way': lease_way,
                'house_type': house_type,
                'toward': toward,
                'address': address,
                'bright_spot': bright_spot,
                'desc': desc,
                'link': link
            }

        except Exception as e:
            print('数据抓取失败：%s, url:%s' % (str(e), link))

    # 二手房信息
    def get_second_hand_infos(self, city):
        url = self.second_hand_url % city
        wb_datas = self.fetch(url)
        soup = BeautifulSoup(wb_datas, 'lxml')
        links = soup.select('h2.title > a')
        infos = []
        for i in links:
            link = i.get('href')
            if link[:2] == '//':
                link = 'https:' + link
            infos.append(self.get_info(link))
        return infos

    def get_second_hand_info(self, link):
        try:
            wb_data = self.fetch(link)
            bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", wb_data)[0]

            soup = BeautifulSoup(wb_data, 'lxml')
            title = soup.select('div.house-title > h1')[0].text.strip()
            basic_item1 = soup.select('p.house-basic-item1 > span')
            total_price = self.show_real_numb(basic_item1[0].text.strip(), bs64_str)
            price_per = self.show_real_numb(basic_item1[1].text.strip(), bs64_str)
            price_per = price_per.replace('\xa0', ' ')

            basic_item2 = soup.select('div.house-basic-item2 > p > span')
            room_main = basic_item2[0].text.strip()
            room_sub = basic_item2[1].text.strip()
            area_main = basic_item2[2].text.strip()
            area_sub = basic_item2[3].text.strip()
            toward_main = basic_item2[4].text.strip()
            toward_sub = basic_item2[5].text.strip()
            toward_sub = toward_sub.replace('\n', '')
            toward_sub = toward_sub.replace(' ', '')
            basic_item3 = soup.select('ul.house-basic-item3 > li > span')
            house_basic1 = basic_item3[1].text.strip().replace('\n', '').replace(' ', '')
            house_basic2 = basic_item3[3].text.strip().replace('\n', '').replace(' ', '')

            return {
                'title': title,
                'total_price': total_price,
                'price_per': price_per,
                'room_main': room_main,
                'room_sub': room_sub,
                'area_main': area_main,
                'area_sub': area_sub,
                'toward_main': toward_main,
                'toward_sub': toward_sub,
                'house_basic1': house_basic1,
                'house_basic2:': house_basic2,
                'link': link
            }

        except Exception as e:
            print('数据抓取失败：%s' % str(e))

    def show_real_numb(self, string, bs64_str):
        font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
        c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
        ret_list = []
        for char in string:
            decode_num = ord(char)
            if decode_num in c:
                num = c[decode_num]
                num = int(num[-2:]) - 1
                ret_list.append(num)
            else:
                ret_list.append(char)
        ret_str_show = ''
        for num in ret_list:
            ret_str_show += str(num)
        return ret_str_show

