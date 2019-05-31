# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/31 10:35

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup
from bs4.element import Tag


class leyoujia(RealEstate):
    def describe(self):
        return self.deep_extend(super(leyoujia, self).describe(), {
            'id': 'leyoujia',
            'name': '乐有家',
            'spelling': True,  # True为全拼，False为缩写
            'has': {
                'fetchNewHouse': True,
                'fetchSecondHandHouse': True,
                'fetchRentalLinks': True
            },
            'urls': {
                'new_house_url': 'https://%s.leyoujia.com/ysl/',
                'second_hand_url': 'https://%s.leyoujia.com/esf/',
                'rental_url': 'https://%s.leyoujia.com/zf/'
            }
        })

    def base_fetch_links(self, url, base_url):
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('p.tit > a')
        links = []
        for i in items:
            link = i.get('href')
            links.append(base_url + link)
        return links

    def fetch_new_hourse_links(self, city):
        if self.has['fetchNewHouse'] == False:
            return None
        url = self.urls['new_house_url'] % city
        base_url = 'https://%s.leyoujia.com' % city
        return self.base_fetch_links(url, base_url)

    def analysis_new_house_page(self, link):
        if self.has['fetchNewHouse'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title_items = soup.select('div.title > h1')
            title = self.format_tag(title_items[0])

            tags_items = soup.select('div.labs > span')
            tags_str = ''
            for i in tags_items:
                tags_str += self.format_tag(i) + '|'

            price_items = soup.select('div.price-box > p')
            price_items = price_items[0].contents
            price = self.format_tag(price_items[3]) + ' ' + self.format_tag(price_items[4])

            intro_list = soup.select('div.intro-list > p > span')
            open_time = self.format_tag(intro_list[1])
            completion_time = self.format_tag(intro_list[3])
            door_model_items = intro_list[9].contents
            door_model = ''
            for i in door_model_items:
                if type(i) == Tag:
                    door_model += self.format_tag(i) + '|'

            door_model = door_model.replace('||', '')
            address = self.format_tag(intro_list[5])

            detail_item = soup.select('p.less')
            detail = self.format_tag(detail_item[0])
            detail = detail.replace('\r', '').replace('\t', '').replace('阅读全文', '')

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

    def fetch_rental_links(self, city):
        if self.has['fetchRentalLinks'] == False:
            return None
        url = self.urls['rental_url'] % city
        base_url = 'https://%s.leyoujia.com' % city
        return self.base_fetch_links(url, base_url)

    def analysis_rental_page(self, link):
        if self.has['fetchRentalLinks'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title_tag = soup.select('h1.tit-conno')
            title = self.format_tag(title_tag[0])

            intro_box1 = soup.select('div.intro-box1 > p')
            price = self.format_tag(intro_box1[0])
            rental_info = self.format_tag(intro_box1[1])
            deposit_way = rental_info.split('|')[0]
            lease_way = rental_info.split('|')[1]

            intro_box2 = soup.select('div.intro-box2 > span')
            house_type = self.format_tag(intro_box2[0])

            intro_box3 = soup.select('div.intro-box3 > p > span')
            address = self.format_tag(intro_box3[3]) + '-' + self.format_tag(intro_box3[1])
            address = address.replace('\r', '').replace('\t', '')

            cont_items = soup.select('div.cont > span')
            area = self.format_tag(cont_items[0])
            area = area.replace('建筑面积', '')
            floor = self.format_tag(cont_items[2])
            floor = floor.replace('所在楼层', '')
            toward = self.format_tag(cont_items[3])
            toward = toward.replace('房屋朝向', '')
            build_time = self.format_tag(cont_items[4])
            build_time = build_time.replace('建筑年代', '')

            desc_items = soup.select('div.fy-box > div.cont > p')

            desc = ''
            for i in desc_items:
                desc += self.format_tag(i)

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
                'build_time': build_time,
                'desc': desc,  # 描述
                'link': link
            }

        except Exception as e:
            print('数据抓取失败：%s, url:%s' % (str(e), link))

    def fetch_second_hand_links(self, city):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        url = self.urls['second_hand_url'] % city
        base_url = 'https://%s.leyoujia.com' % city
        return self.base_fetch_links(url, base_url)

    def analysis_second_hand_page(self, link):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'lxml')
            title_tag = soup.select('h1.tit-conno')
            title = self.format_tag(title_tag[0])
            base_span_items = soup.select('div.intro > div > span')
            total_price = self.format_tag(base_span_items[0])
            toward = self.format_tag(base_span_items[3])
            area = self.format_tag(base_span_items[2])
            door_model = self.format_tag(base_span_items[1])
            floor = self.format_tag(base_span_items[4])
            build_time = self.format_tag(base_span_items[6])

            base_p_items = soup.select('div.intro-box3 > p > span')
            community = self.format_tag(base_p_items[3])
            community = community.replace('\r', '').replace('\t', '')
            address = self.format_tag(base_p_items[5])
            address = address.replace('\r', '').replace('\t', '')

            price_per_item = soup.select('div.intro-box1 > div')
            price_per = self.format_tag(price_per_item[0])
            price_per = price_per.replace('单价', '')

            cont_items = soup.select('p.mb10 > span')
            house_type = self.format_tag(cont_items[6])
            house_type = house_type.replace('用途', '')
            equity_year = self.format_tag(cont_items[10])
            equity_year = equity_year.replace('产权年限', '')
            equity_type = self.format_tag(cont_items[8])
            equity_type = equity_type.replace('产权性质', '')
            fitment = self.format_tag(cont_items[12])
            fitment = fitment.replace('装修', '')

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
