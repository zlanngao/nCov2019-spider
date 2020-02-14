# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/12 13:06
# @Function:

import requests
import csv
from lxml import etree

url_dict = {
    '广东省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_guangdong.json?v=1581483742936',
    '云南省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_yunnan.json?v=1581487361231',
    '河南省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_henan.json?v=1581487439669',
    '贵州省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_guizhou.json?v=1581487476511',
    '四川省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_sichuan.json?v=1581487501838',
    '天津市':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_tianjin.json?v=1581487553135',
    '安徽省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_anhui.json?v=1581487581807',
    '江西省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_jiangxi.json?v=1581487605871',
    '河北省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_hebei.json?v=1581487630618',
    '北京市': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_beijing.json?v=1581487651824',
    '福建省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_fujian.json?v=1581487707950',
    '浙江省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_zhejiang.json?v=1581487728115',
    '江苏省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_jiangsu.json?v=1581487763038',
    '山西省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_shanxi.json?v=1581487793784',
    '吉林省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_jilin.json?v=1581487836894',
    '陕西省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_shaanxi.json?v=1581487865138',
    '内蒙古': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_neimenggu.json?v=1581487917950',
    '山东省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_shandong.json?v=1581487945952',
    '重庆市':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_chongqing.json?v=1581487983441',
    '海南省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_hainan.json?v=1581488002450',
    '湖南省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_hunan.json?v=1581488024092',
    '辽宁省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_liaoning.json?v=1581488042394',
    '甘肃省': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_gansu.json?v=1581488066333',
    '宁夏': 'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_ningxia.json?v=1581488097003',
    '上海市':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_shanghai.json?v=1581488137988',
    '广西省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_guangxi.json?v=1581488158912',
    '黑龙江省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_heilongjiang.json?v=1581488177348',
    '青海省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_qinghai.json?v=1581488196544',
    '湖北省':'https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_hubei.json?v=1581488211399'
}


def get_information(url):
    print(url)
    if url == None:
        return ''
    try:
        res = requests.get(url)
        select = etree.HTML(res.text)

        title = ','.join(select.xpath('//*[@id="activity-name"]/text()'))
        text = '。'.join(select.xpath('//*[@id="js_content"]/p/span/text()'))

        if title == '':
            title = ','.join(select.xpath('//*[@id="TitleSection"]/h2/text()'))
        if text == '':
            text = ','.join(select.xpath('//*[@id="docContent"]/p/text()'))

        return title, text
    except Exception as e:
        print(e)
        return ''


if __name__ == '__main__':

    for province in url_dict:

        print(province)
        res = requests.get(url_dict[province])

        with open("chinadata/{}.csv".format(province), "a+", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['city','district','street','place','location','remark','source','link','is_today','title','text','province'])
            if res.json()['errcode'] == 0:
                for line in res.json()['data']:
                    # 市
                    town_total_place = line['total_place']
                    for district_ in line['districtList']:
                        # 县
                        county_total_place = district_['total_place']
                        for place in district_['placeList']:
                            written = place
                            print(place)
                            #written = dict({'province':province}.items()+place.items)#字典前加一个省份字段
                            if place['link'] != None:
                                link = place['link']
                            else:
                                link = ''
                            # title, text = get_information(link)
                            written['title'] = ''
                            written['text'] = ''
                            written['province'] = province
                            writer.writerow(written.values())


            else:
                print(res.json()['errmsg'])
