#！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/31 10:32

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup


class qfang(RealEstate):
    def describe(self):
        return self.deep_extend(super(qfang, self).describe(), {
            'id': 'qfang',
            'name': 'Q房网',
            'spelling': True,  # True为全拼，False为缩写
            'has': {
                'fetchNewHouse': True,
                'fetchSecondHandHouse': True,
                'fetchRentalLinks': True
            },
            'urls': {
                'new_house_url': 'https://%s.qfang.com/newhouse/list',
                'second_hand_url': 'https://%s.qfang.com/sale',
                'rental_url': 'https://%s.qfang.com/rent'
            }
        })

    def fetch_new_hourse_links(self, city):
        if self.has['fetchNewHouse'] == False:
            return None

        url = self.urls['new_house_url'] % city
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('div.house-title > a')
        links = []
        for i in items:
            link = i.get('href')
            links.append(link)
        return links

    def analysis_new_house_page(self, link):
        if self.has['fetchNewHouse'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title = self.format_tag(soup.select('div.left-con > h2')[0])
            tag_items = soup.select('div.left-con > div > div')
            tags = []
            for item in tag_items:
                tags.append(self.format_tag(item))

            basic_info_items = soup.select('div.basic-info > ul > li.clearfix > p')
            price = self.format_tag(basic_info_items[4])
            open_time = self.format_tag(basic_info_items[12])
            completion_time = self.format_tag(basic_info_items[14])
            # TODO
            door_model = None

            address = self.format_tag(basic_info_items[-2])
            detail = None
            return {
                'title': title,
                'tags': ','.join(tags),  # 标签
                'price': price,  # 单位价格
                'open_time': open_time,  # 开盘时间
                'completion_time': completion_time,  # 交房时间
                'door_model': door_model,  # 户型
                'address': address,  # 地址
                'detail': detail,  # 简介
                'link': link
            }

        except Exception as e:
            print('数据抓取失败：%s, url:%s' % (str(e), link))

    def fetch_rental_links(self, city):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        url = self.urls['second_hand_url'] % city
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('p.house-title > a')
        links = []
        for i in items:
            link = i.get('href')
            links.append(link)
        return links

    def analysis_rental_page(self, link):
        pass

    def fetch_second_hand_links(self, city):
        pass

    def analysis_second_hand_page(self, link):
        pass



f = qfang()
print(f.fetch_rental_links('shenzhen'))