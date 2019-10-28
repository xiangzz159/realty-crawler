# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/5/31 10:29

@desc:

'''

from base.realestate import RealEstate
from bs4 import BeautifulSoup


class fang(RealEstate):
    def describe(self):
        return self.deep_extend(super(fang, self).describe(), {
            'id': 'fang',
            'name': '房天下',
            'spelling': False,  # True为全拼，False为缩写
            "timeout": 20000,
            'has': {
                'fetchNewHouse': True,
                'fetchSecondHandHouse': True,
                'fetchRentalLinks': True
            },
            'urls': {
                'new_house_url': 'https://%s.newhouse.fang.com/house/s/',
                'second_hand_url': 'https://%s.esf.fang.com/',
                'rental_url': 'https://%s.zu.fang.com/'
            }
        })

    def fetch_new_house_home_links(self, url, city):
        home_links = []
        base_url = 'https://%s.newhouse.fang.com' % city if city != 'bj' else 'https://newhouse.fang.com'
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        page_items = soup.select('li.fr > a')
        for i in page_items:
            if i.has_attr('class'):
                continue
            link = base_url + i.get('href')
            home_links.append(link)
        return home_links

    def fetch_new_hourse_links(self, city):
        if self.has['fetchNewHouse'] == False:
            return None
        url = self.urls['new_house_url'] % city if city != 'bj' else 'https://newhouse.fang.com/house/s/'
        home_urls = []
        while True:
            home_urls_ = self.fetch_new_house_home_links(url, city)
            if home_urls_[-1] in home_urls:
                break
            url = home_urls_[-1]
            home_urls += home_urls_

        home_urls = set(home_urls)
        links = []
        for i in home_urls:
            wb_data = self.fetch(i)
            soup = BeautifulSoup(wb_data, 'lxml')
            items = soup.select('div.house_value > div.nlcd_name > a')
            for i in items:
                link = i.get('href')
                if link[:2] == '//':
                    link = 'https:' + link
                links.append(link)
        return links

    def analysis_new_house_page(self, link):
        if self.has['fetchNewHouse'] == False:
            return None
        # TODO
        pass

    def fetch_rental_links(self, city):
        if self.has['fetchRentalLinks'] == False:
            return None
        url = self.urls['rental_url'] % city if city != 'bj' else 'https://zu.fang.com/'
        wb_data = self.fetch(url)
        soup = BeautifulSoup(wb_data, 'lxml')
        items = soup.select('p.title > a')
        links = []
        base_url = 'https://%s.zu.fang.com' % city if city != 'bj' else 'https://zu.fang.com/'
        for i in items:
            link = i.get('href')
            links.append(base_url + link)
        return links

    def analysis_rental_page(self, link):
        if self.has['fetchRentalLinks'] == False:
            return None
        try:
            wb_data = self.fetch(link)
            soup = BeautifulSoup(wb_data, 'html.parser')
            title_tag = soup.select('h1.title')
            title = self.format_tag(title_tag[0])
            price_tag = soup.select('div.trl-item')
            price_strs = self.format_tag(price_tag[0]).split('(')
            price = price_strs[0]
            deposit_way = price_strs[0][:-1]
            base_info_tags = soup.select('div.trl-item1 > div')
            lease_way = None
            house_type = None
            toward = None
            address = None
            area = None
            floor = None
            desc = None

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

    def fetch_second_hand_links(self, city):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        pass

    def analysis_second_hand_page(self, link):
        if self.has['fetchSecondHandHouse'] == False:
            return None
        pass
