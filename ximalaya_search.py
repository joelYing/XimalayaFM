#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-16
import os
import time
import pymongo
import random
import requests
import re


'''
'https://www.ximalaya.com/category/'  所有分类
'https://www.ximalaya.com/revision/play/tracks?trackIds=90616407'  获取源音频的api
'''


class XiMa(object):
    def __init__(self):
        self.category_Url = 'https://www.ximalaya.com/category/'
        self.base_url = 'https://www.ximalaya.com'
        self.base_api = 'https://www.ximalaya.com/revision/play/tracks?trackIds='
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
        self.s = requests.session()

    def get_fm_music(self, fm_url):
        print(fm_url)
        r = self.s.get(fm_url, headers=self.header)
        title = re.findall(r'<h1 class="title PIuT">(.*?)</h1>', r.text, re.S)
        max_page = re.findall(r'<form class="tthf"><input type="number" placeholder="请输入页码" step="1" min="1" '
                              r'max="(\d+)" class="control-input tthf" value=""/>', r.text, re.S)
        if max_page and max_page[0]:
            for page in range(1, int(max_page[0]) + 1):
                fm_urls = fm_url + '/p{}'.format(page)
                r = self.s.get(fm_urls, headers=self.header)
                self.get_detail(r.text, title)
        else:
            self.get_detail(r.text, title)

    def get_detail(self, text, title):
        track_list = re.findall(r'<div class="text rC5T"><a title="(.*?)" href="(.*?)">.*?'
                                r'<i class="xuicon xuicon-erji1 rC5T"></i>(.*?)</span></div>'
                                r'<span class="time rC5T">(.*?)</span>',
                                text, re.S)
        # 爬取一个FM下的每个音频
        for i in track_list:
            print(i)
            # 获取爬取音频所需的trackIds
            music_title = i[0]
            music_url = self.base_url + i[1]
            listen_num = i[2]
            create_time = i[3]
            trackid = str(i[1]).split('/')[3]
            # api中的数据信息
            api = self.base_api + trackid
            print(api)
            r = self.s.get(api, headers=self.header)
            result = r.json()
            src = result['data']['tracksForAudioPlay'][0]
            if src['src']:
                print(u'试听')
                r = self.s.get(src['src'], headers=self.header)
                path = '/home/joel/XiMa/' + title[0]
                e = os.path.exists(path)
                if not e:
                    os.mkdir(path)
                fm_path = path + '/{}.m4a'.format(src['trackName'])
                if not os.path.exists(fm_path):
                    with open(path + '/{}.m4a'.format(src['trackName']), 'wb') as f:
                        f.write(r.content)
                        print(u'保存完毕...')
                else:
                    print(u'm4a已存在')
            else:
                print(u'需要收费')


if __name__ == '__main__':
    xima = XiMa()
    url = input(u'请输入要获取喜马拉雅节目第一页的网址：')
    xima.get_fm_music(url)
