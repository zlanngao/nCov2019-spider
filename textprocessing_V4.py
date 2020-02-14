# -*- coding: utf-8 -*-
# @Author  : 刘天勇
# @Time    : 2020/2/11 13:17
# @Function:


from __future__ import print_function, unicode_literals
import json
import requests
import pandas as pd
import csv
import re


# 备用key
# tokenid=['M4Th_Znq.9902.yv4gRv5hJhWh'
#           ,'0bGs1eLu.9911.MVXdu3KQ2P2j'
#           ,'ouonDx-z.10033.aUxahjJzOTGO'
#           ,'ARcMMACb.10037.2t0e2YRvn6cC'
#           ,'KRqOmkrG.10043.yA2GmkqgeN5Z'
#           ,'cVFItZRN.10045.rARuZMsDeCay'
#           ,'BpvxYQof.10050.TRxkjC8ifQvh'
#           ,'_fWktNtl.10051.PDjOm-JhWABX'
#           ,'jMfULdKN.10052.qCO4gMChWYEO'
#           ,'MzunFfGy.10054.Gow1hXSqgkVW'
#           ,'BHu56kuq.10059.HsD0PHhFnbll'
#           ,'uWKqyd9e.10062.iUlnr6Vkzgnd']

def matching_year(text):
    return ''.join(re.findall('(\d+年)', text))


def matching_month(text):
    return ''.join(re.findall('(\d+月)', text))


def matching_day(text):
    day = ''.join(re.findall('\d+月(\d+日至\d+日)', text))
    if day != '':
        return day

    day = ''.join(re.findall('(\d+日)', text))
    if day != '':
        return day

    return ''


def read_data(path, type='csv'):
    if type == 'csv':
        df = pd.read_csv(path,encoding='utf-8')
        return df
    if type == 'xlsx':
        df = pd.read_excel(path)
        return df


def get_NER(ids, texts):
    data = json.dumps(texts)
    headers = {
        'X-Token': 'BHu56kuq.10059.HsD0PHhFnbll',
        'Content-Type': 'application/json'
    }
    NER_URL = 'http://api.bosonnlp.com/ner/analysis'
    resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))
    print(resp.text)
    with open("textprocessing/海南省.csv", "a+", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for id, text, item in zip(ids, texts, resp.json()):

            ner_list = []
            for entity in item['entity']:
                ner_name = ''.join(item['word'][entity[0]:entity[1]])
                ner_class = ''.join(entity[2])
                ner_list.append(ner_name + '#' + ner_class)

            written = []
            last_time = ''
            last_time_year = '2020年'
            last_time_month = matching_month(ner_list[0])
            last_time_day = matching_day(ner_list[0])

            for ner in ner_list:
                ner_class = ner.split('#')[1]
                ner_name = ner.split('#')[0]

                if ner_class == 'time':
                    last_time = ner_name
                elif ner_class == 'location':
                    year = matching_year(last_time)
                    month = matching_month(last_time)
                    day = matching_day(last_time)

                    new_time = ''
                    # 缺少年月日
                    if day == '' and month == '' and year == '':
                        new_time = last_time_year + last_time_month + last_time_day + last_time
                    elif month == '' and year == '':
                        last_time_day = day
                        new_time = last_time_year + last_time_month + last_time
                    elif year == '':
                        last_time_month = month
                        last_time_day = day
                        new_time = last_time_year + last_time
                    else:
                        new_time = last_time

                    writer.writerow([id, text, new_time, ner_name])

            # for i in range(-1, -5, -1):
            #     end_time = matching_day(ner_list[-1])
            #     if end_time != '':
            # #         break
            # writer.writerow([id, text, last_time_year + last_time_month + last_time_day, '确诊'])


if __name__ == '__main__':
    df = read_data('datadetail/海南省.csv', 'csv')
    texts = df['活动路径']
    ids = df['病例']

    req_texts = list(texts)
    ids = list(ids)

    get_NER(ids[:100], req_texts[:100])
    get_NER(ids[100:], req_texts[100:])
