#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-16
import os
import time
import pymongo
import random
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

'''
'https://www.ximalaya.com/category/'  所有分类
'https://www.ximalaya.com/revision/play/tracks?trackIds=90616407'  获取源音频的api
'''
category_Url = 'https://www.ximalaya.com/category/'
base_url = 'https://www.ximalaya.com'
base_api = 'https://www.ximalaya.com/revision/play/tracks?trackIds='
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['ximalaya']


def getUrl():
    r = requests.get(category_Url, headers=header)
    html = r.text
    result = re.findall(r'<a class="e-2880429693 item separator".*?href="(.*?)">(.*?)</a>', html, re.S)
    url_list = []
    for i in result:
        # 以一个分类为例  - - 有声书中的文学类，若没有break 则可获取全部分类
        second_url = base_url + i[0]
        url_list.append(second_url)
        # 获取该分类中全部的页数
        getMorePage(second_url)
        print second_url
        break
    # print url_list


def getMusicList(url, page):
    r = requests.get(url, headers=header)
    m_list_html = r.text
    result = re.findall(
        r'<a class="e-1889510108.*?href="(.*?)"><img.*?src="(.*?)".*?alt="(.*?)".*?/>.*?"e-1889510108 icon-earphone xuicon xuicon-erji"></i>(.*?)</span>.*?"e-2896848410 album-author".*?title="(.*?)">',
        m_list_html, re.S)
    info = []
    # 获取该page中每一个FM的数据信息，可以存入MongoDB
    for i in result:
        FM_info = {}
        FM_url = base_url + i[0]
        FM_info['url'] = FM_url
        FM_info['picture'] = i[1]
        FM_info['name'] = i[2]
        FM_info['playback'] = i[3]
        FM_info['author'] = i[4]
        info.append(FM_info)
        # 获取该FM中的音频信息
        # os.mkdir('D:\\Python\\PycharmProject\\Enhance\\xmly_fm\\{}'.format(FM_info['name']))
        get_FM_music(FM_url)
        # 先获取一个FM

    # for j in info:
    #     print j
    test = db['page' + str(page)]
    test.insert(info)


def get_FM_music(fm_url):
    print fm_url
    r = requests.get(fm_url, headers=header)
    FM_music_html = r.text
    track_list = re.findall(r'<div class="e-2304105070 text"><a.*?title="(.*?)".*?href="(.*?)">.*?</a>', FM_music_html,re.S)
    detail_info = []
    # 爬取一个FM下的每个音频
    j = 1
    for i in track_list:
        detail = {}
        # 获取爬取音频所需的trackIds
        id = str(i[1]).split('/')[3]
        detail['title'] = i[0]
        detail['detail_url'] = base_url + i[1]
        detail_info.append(detail)
        # api中的数据信息
        get_detailFM_api(id)
        print u'已获取第' + str(j) + u'个音频'
        j += 1
    print detail['title']+u',该音频爬取完毕'
    time.sleep(2+random.randint(1,10))


def get_detailFM_api(id):
    api = base_api + id
    print api
    r = requests.get(api, headers=header)
    result = r.json()
    src = result['data']['tracksForAudioPlay'][0]
    if src['src']:
        print u'试听'
        r = requests.get(src['src'], headers=header)
        try:
            f = open('D:\\Python\\PycharmProject\\Enhance\\xmly_fm\\{}.m4a'.format(src['trackName']),'wb')
        except:
            print u'已存在'
            pass
        f.write(r.content)
        f.close
        print u'保存完毕...'
    else:
        print u'需要收费'
        pass



def getMorePage(url):
    r = requests.get(url, headers=header)
    m_list_html = r.text
    pageNum = re.findall(r'(\d+)</span></a></li><li class="e-3793817119 page-next page-item">', m_list_html,re.S)
    pageNum = int(pageNum[0])
    # 循环获取每一页，这里暂时获取第一页
    for i in range(1, pageNum + 1):
        if i == 1:
            page_url = url
            # 获取页中的30个FM
            getMusicList(page_url, i)
        else:
            page_url = url + 'p{}/'.format(i)
            getMusicList(page_url, i)
        #爬取一页
        break


if __name__ == '__main__':
    getUrl()
