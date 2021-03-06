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


class anjuke(RealEstate):

    def describe(self):
        return self.deep_extend(super(anjuke, self).describe(), {
            'id': 'anjuke',
            'name': '安居客',
            'spelling': False,      # True为全拼，False为缩写
            'has': {
                'fetchNewHouse': True,
                'fetchSecondHandHouse': True,
                'fetchRentalLinks': True
            },
            'urls': {
                'new_house_url': 'https://%s.fang.anjuke.com/',
                'second_hand_url': 'https://%s.anjuke.com/sale/',
                'rental_url': 'https://%s.zu.anjuke.com/'
            }
        })

    # 新房信息
    def fetch_new_hourse_links(self, city):
        if self.has['fetchNewHouse'] == False:
            return None

        url = self.urls['new_house_url'] % city
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('div.key-list > div.item-mod')
        links = []
        for i in items:
            link = i.get('data-link')
            links.append(link)
        return links

    def analysis_new_house_page(self, link):
        if self.has['fetchNewHouse'] == False:
            return None

        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title = self.format_tag(soup.select('div.basic-info > h1')[0])
            base_params = soup.select('dl.basic-parms > dd')
            item0_lst = list(base_params[0].descendants)
            item1_lst = list(base_params[1].descendants)
            item2_lst = list(base_params[2].descendants)
            item3_lst = list(base_params[3].descendants)
            item4_lst = list(base_params[4].descendants)

            tags = soup.select('div.tags > a')
            tags_str = ''
            for i in tags:
                tags_str += self.format_tag(i) + '|'

            price = item0_lst[4] + ' ' + item0_lst[6]
            open_time = item1_lst[1]
            completion_time = item2_lst[2]
            door_model = item3_lst[4]
            address = item4_lst[2]
            detail = soup.select('div.louping-detail')[0].text.strip().replace('\n', '').replace(' ', '')
            return {
                'title': title,
                'tags': tags_str,  # 标签
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

    # 二手房信息
    def fetch_second_hand_links(self, city):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        url = self.urls['second_hand_url'] % city
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('div.house-title > a')
        links = []
        for i in items:
            link = i.get('href')
            links.append(link)
        return links

    def analysis_second_hand_page(self, link):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')

            title = soup.select('h3.long-title')[0].text.strip().replace('\n', '').replace(' ', '')
            base_infos = soup.select('div.houseInfo-wrap > ul > li > div.houseInfo-content')
            community = self.format_tag(base_infos[0])
            door_model = self.format_tag(base_infos[1])
            door_model = door_model.replace('\t', '')
            price_per = self.format_tag(base_infos[2])
            address = self.format_tag(base_infos[3])
            address = address.replace('\ue003', '')
            area = self.format_tag(base_infos[4])
            build_time = self.format_tag(base_infos[6])
            toward = self.format_tag(base_infos[7])
            house_type = self.format_tag(base_infos[9])
            floor = self.format_tag(base_infos[10])
            fitment = self.format_tag(base_infos[11])
            equity_year = self.format_tag(base_infos[12])
            equity_type = self.format_tag(base_infos[15])

            simple_infos = soup.select('div.basic-info > span')
            total_price = self.format_tag(simple_infos[0])

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
                'house_type': house_type,  # 房屋类型
                'floor': floor,  # 所在楼层
                'fitment': fitment,  # 装修程度
                'equity_year': equity_year,  # 产权年限
                'equity_type': equity_type,  # 产权性质
                'link': link  # 链接地址
            }

        except Exception as e:
            print('数据抓取失败：%s, url:%s' % (str(e), link))

    # 租房信息
    def fetch_rental_links(self, city):
        if self.has['fetchRentalLinks'] == False:
            return None
        url = self.urls['rental_url'] % city
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('div.zu-itemmod')
        links = []
        for i in items:
            link = i.get('link')
            links.append(link)
        return links

    def analysis_rental_page(self, link):
        if self.has['fetchRentalLinks'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title = soup.select('h3.house-title')
            title = self.format_tag(title[0])

            simple_infos = soup.select('ul.title-label > li')
            lease_way = self.format_tag(simple_infos[0])
            toward = self.format_tag(simple_infos[1])

            basic_infos = soup.select('ul.house-info-zufang > li')
            item0_lst = basic_infos[0].contents
            item2_lst = basic_infos[2].contents
            item4_lst = basic_infos[4].contents
            item6_lst = basic_infos[6].contents

            price = self.format_tag(item0_lst[1])
            deposit_way = self.format_tag(item0_lst[3])
            house_type = self.format_tag(item6_lst[3])
            address = self.format_tag(basic_infos[7])
            address = address.split('：')[1].replace('\xa0', '')
            floor = self.format_tag(item4_lst[3])
            area = self.format_tag(item2_lst[3])
            desc = self.format_tag(soup.select('div.auto-general')[0])

            return {
                'title': title,
                'price': price,  # 月租
                'deposit_way': deposit_way,  # 押金方式：押二付一
                'lease_way': lease_way,  # 租借方式：整租/合租
                'house_type': house_type,  # 房屋类型
                'toward': toward,  # 朝向
                'address': address,  # 地址
                'area': area,
                'floor': floor,
                'build_time': None,
                'desc': desc,  # 描述
                'link': link
            }
        except Exception as e:
            print('数据抓取失败：%s, url:%s' % (str(e), link))
