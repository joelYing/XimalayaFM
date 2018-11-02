#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-11-2

import os
import requests
import re


class XiMa(object):
    """
    'https://www.ximalaya.com/category/'  所有分类
    'https://www.ximalaya.com/revision/play/tracks?trackIds=90616407'  获取源音频的api
    """
    def __init__(self):
        self.category_Url = 'https://www.ximalaya.com/category/'
        self.base_url = 'https://www.ximalaya.com'
        self.base_api = 'https://www.ximalaya.com/revision/play/tracks?trackIds='
        self.header = {
            'User-Agent': 'your-user-agent'
        }
        self.s = requests.session()

    def geturl(self):
        r = self.s.get(self.category_Url, headers=self.header)
        result = re.findall(r'<a class="item separator Kx" href="(.*?)">(.*?)</a>', r.text, re.S)
        url_list = []
        for i in result:
            # 以一个分类为例  - - 有声书中的文学类，若没有break 则可获取全部分类
            second_url = self.base_url + i[0]
            url_list.append(second_url)
            # 获取该分类中全部的页数
            print(second_url, i[1])
            self.get_more_page(second_url)
            break
        # print url_list

    def get_more_page(self, url):
        r = self.s.get(url, headers=self.header)
        pagenum = re.findall(r'<input type="number" placeholder="请输入页码" step="1" min="1" '
                             r'max="(\d+)" class="control-input tthf" value=""/>', r.text, re.S)
        pagenum = int(pagenum[0])
        # 循环获取每一页，这里暂时获取第一页
        for i in range(1, pagenum + 1):
            print(u'第' + str(i) + u'页')
            page_url = url + 'p{}/'.format(i)
            self.get_music_list(page_url)
            # 爬取一页
            break

    def get_music_list(self, url):
        r = self.s.get(url, headers=self.header)
        result = re.findall(
            r'<a xm_other_props="\[object Object]" class="album-cover.*?" href="(.*?)"><img src="(.*?)" alt="(.*?)" '
            r'class="EV"/>.*?<a xm_other_props="\[object Object]" class="album-author Iki" title="(.*?)" href=".*?">',
            r.text, re.S)
        info = []
        # 获取该page中每一个FM的数据信息
        for i in result:
            fm_info = {}
            fm_url = self.base_url + i[0]
            fm_info['url'] = fm_url
            fm_info['picture'] = 'https:' + str(i[1]).replace('amp;', '')
            fm_info['fm_name'] = i[2]
            fm_info['author'] = i[3]
            info.append(fm_info)
            print(fm_info)
            # 获取该FM中的音频信息
            self.get_fm_music(fm_url)
            # 先获取一个FM

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
    xima.geturl()
