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
    def fetch_rental_links(self, city):
        url = self.rental_url % (city)
        wb_datas = self.fetch(url)
        soup = BeautifulSoup(wb_datas, 'lxml')
        items = soup.select('ul.house-list > li > div.des > h2 > a')
        links = []
        for i in items:
            link = i.get('href')
            if 'e.58.com' in link:
                continue
            if link[:2] == '//':
                link = 'https:' + link
            links.append(link)
        return links

    def analysis_rental_page(self, link):
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
            lease_way = self.format_tag(base_desc[1])
            house_type = self.format_tag(base_desc[3])
            house_type = house_type.replace('\xa0\xa0', ' ')
            house_type = self.show_real_numb(house_type, bs64_str)
            toward = self.format_tag(base_desc[5])
            toward = toward.replace('\xa0\xa0', ' ')
            toward = self.show_real_numb(toward, bs64_str)
            address1 = self.format_tag(base_desc[7])
            area = self.format_tag(base_desc[9])
            address2 = self.format_tag(base_desc[11])
            address = area + '_' + address2 + '_' + address1
            address = address.replace('\xa0\xa0', ' ')

            introduce_item = soup.select('ul.introduce-item > li')
            bright_spot = self.format_tag(introduce_item[0])
            desc = self.format_tag(introduce_item[1])
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
    def fetch_second_hand_links(self, city):
        url = self.second_hand_url % city
        wb_datas = self.fetch(url)
        soup = BeautifulSoup(wb_datas, 'lxml')
        items = soup.select('h2.title > a')
        links = []
        for i in items:
            link = i.get('href')
            if link[:2] == '//':
                link = 'https:' + link
            links.append(link)
        return links

    def analysis_second_hand_page(self, link):
        try:
            wb_data = self.fetch(link)
            bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", wb_data)[0]

            soup = BeautifulSoup(wb_data, 'lxml')
            title = self.format_tag(soup.select('div.house-title > h1')[0])
            basic_item1 = soup.select('p.house-basic-item1 > span')
            total_price = self.show_real_numb(basic_item1[0].text.strip(), bs64_str)
            price_per = self.show_real_numb(basic_item1[1].text.strip(), bs64_str)
            price_per = price_per.replace('\xa0', ' ')

            basic_item2 = soup.select('div.house-basic-item2 > p > span')
            door_model = self.format_tag(basic_item2[0])
            floor = self.format_tag(basic_item2[1])
            area = self.format_tag(basic_item2[2])
            fitment = self.format_tag(basic_item2[3])
            toward = self.format_tag(basic_item2[4])
            build_time = self.format_tag(basic_item2[5])

            basic_item3 = soup.select('ul.house-basic-item3 > li > span')
            community = self.format_tag(basic_item3[1])
            address = self.format_tag(basic_item3[3])

            general_item = soup.select('ul.general-item-right > li > span')
            equity_year = self.format_tag(general_item[5])

            return {
                'title': title,  # 标题
                'total_price': total_price,  # 总价
                'price_per': price_per,  # 房屋单价
                'community': community,  # 所属小区
                'door_model': door_model,  # 户型
                'address': address,  # 地址
                'area': area,  # 建筑面积
                'build_time': build_time,  # 建造年代
                'toward': toward,  # 朝向
                'house_type': '普通住宅',  # 房屋类型
                'floor': floor,  # 所在楼层
                'fitment': fitment,  # 装修程度
                'equity_year': equity_year,  # 产权年限
                'equity_type': '商品房',  # 产权性质
                'link': link  # 链接地址
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