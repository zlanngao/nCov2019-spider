# -*- coding: utf-8 -*-
# @Author  : 高华玲
# @Time    : 2020/2/13 13:06
# @Function:将全国各个省的数据表合并为allchinadata.csv，并统计链接来源


import glob
import os
import pandas as pd

inputfile = str(os.path.dirname(os.getcwd())) + "\spider" + "\chinadata\*.csv"
outputfile =  str(os.path.dirname(os.getcwd()))+ "\spider" + "\\allchinadata.csv"
csv_list = glob.glob(inputfile)
filepath =  csv_list [0]
#filename = filepath.split('\\')[-1].split('.')[0]
#print(filename)
df = pd.read_csv(filepath,encoding="utf8",low_memory=False)#读取第一个文件
#df.insert(0,'province',"")#插入一列名
df = df.to_csv(outputfile,encoding="utf8",index=False)
print(filepath)
for i in range(1,len(csv_list)):
    filepath = csv_list [i]
    #filename = filepath.split('\\')[-1].split('.')[0]     #获取文档名称中的省份名
    df = pd.read_csv(filepath,encoding="utf8",low_memory=False)
    #df.insert(0,'province',filename) #第一列插入为0,列名’province’，全赋值为每个csv的文件名
    #print(filename)
    df.to_csv(outputfile,encoding="utf8",index=False,mode='a+',header=False)

#处理所有的url，统计域名，去重
df = pd.read_csv(outputfile,usecols=['link'],encoding="utf8",low_memory=False)#仅取出link列
df['link'] = df['link'].astype(str)#转换某一列数据类型
df['link'] = df['link'].apply(lambda x:x.split('/')[0:3])#将通过apply方法中的匿名函数进行数据的处理
df.to_csv("url.csv",index=False, encoding='utf-8')


