# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/22 19:24

@desc:

'''

from bs4 import BeautifulSoup
import requests
import config
from fontTools.ttLib import TTFont
from io import BytesIO
import base64
import re


def get_city_all_infos(city):
    url = 'https://%s.58.com/ershoufang/' % city
    wb_datas = requests.get(url, headers=config.headers)
    soup = BeautifulSoup(wb_datas.text, 'lxml')
    links = soup.select('h2.title > a')
    for i in links[:1]:
        link = i.get('href')
        if link[:2] == '//':
            link = 'https:' + link
        print(link)
        get_info(link)
        print('*' * 50)


def get_info(link):
    try:
        wb_data = requests.get(link, headers=config.headers)
        bs64_str = re.findall("charset=utf-8;base64,(.*?)'\)", wb_data.text)[0]

        soup = BeautifulSoup(wb_data.text, 'lxml')
        data_dict = {}
        title = soup.select('div.house-title > h1')[0].text.strip()
        basic_item1 = soup.select('p.house-basic-item1 > span')
        total_price = get_page_show_ret(basic_item1[0].text.strip(), bs64_str)
        price_per = get_page_show_ret(basic_item1[1].text.strip(), bs64_str)
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

        data_dict = {
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
            'house_basic2:': house_basic2
        }
        print(data_dict)

    except Exception as e:
        print('数据抓取失败：%s' % str(e))


def get_page_show_ret(string, bs64_str):
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


get_city_all_infos('sz')
