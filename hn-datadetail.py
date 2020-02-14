import requests
from lxml import etree
import pandas as pd
import re

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}


if __name__ == '__main__':
    url = 'http://wst.hainan.gov.cn/yqfk/index/index/qianyi.html'

    res = requests.get(url)
    selector = etree.HTML(res.text)
    title = selector.xpath('/html/body/div/div/div/div/h3/span/text()')
    text = selector.xpath('/html/body/div/div/div/div/div/text()')

    df = pd.DataFrame()

    case = []
    message = []
    pathway = []

    for i,j in zip(title,text):
        text = ''.join(''.join(j).split())
        case_id = ''.join(re.findall('第(\d+号)确诊病例',text.split('，')[0]))
        case.append(case_id)
        print(text.split('。')[0])
        message.append(text.split('。')[0].replace(text.split('，')[0]+'，',''))
        pathway.append(''.join(text.split('。')[1:]))

    df['病例'] = case
    df['基本信息'] = message
    df['活动路径'] = pathway

    # df = pd.concat([old_df,df],axis=0)
    # df = df.drop_duplicates(['活动路径'])

    df.to_csv('datadetail/海南省.csv',index=False)


