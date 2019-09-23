#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 19-9-22

import hashlib
import json
import math
import os
import re
import time
import random
import requests

"""
注意请修改 make_dir() 中的下载路径
"""


class XiMa(object):
    def __init__(self):
        self.base_url = 'https://www.ximalaya.com'
        self.base_api = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort=0&pageSize=30'
        self.time_api = 'https://www.ximalaya.com/revision/time'
        # 获取付费节目总音源个数与节目名
        self.pay_api = 'https://www.ximalaya.com/revision/album?albumId={}'
        # 获取每一页付费音源的ID等信息
        self.pay_api_2 = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'
        # APP抓包得到，可用于获取付费节目总音源个数与节目名，获取音集所有音频ID，通过改变pageSize的大小，（albumId, pageSize）
        self.pay_api_allinfo = 'http://180.153.255.6/mobile-album/album/page/ts-1569206246849?ac=WIFI&albumId={}' \
                               '&device=android&isAsc=true&isQueryInvitationBrand=true&isVideoAsc=true&pageId=1' \
                               '&pageSize={}'
        # 获取单个付费音频api （trackId）
        self.pay_api_single = 'http://mobile.ximalaya.com/mobile/redirect/free/play/{}/2'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
        self.s = requests.session()

    def get_time(self):
        """
        获取服务器时间戳
        :return:
        """
        r = self.s.get(self.time_api, headers=self.header)
        return r.text

    def get_sign(self):
        """
        获取sign： md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :return: xm_sign
        """
        nowtime = str(round(time.time() * 1000))
        servertime = self.get_time()
        sign = str(hashlib.md5("ximalaya-{}".format(servertime).encode()).hexdigest()) + "({})".format(
            str(round(random.random() * 100))) + servertime + "({})".format(str(round(random.random() * 100))) + nowtime
        self.header["xm-sign"] = sign
        # print(sign)
        # return sign

    def index_choose(self):
        c_num = input(u'请输入对应操作的选项：\n'
                      u'1、下载整部有声书\n'
                      u'2、下载单个音源\n'
                      u'3、下载已付费有声书\n'
                      u'4、返回\n')
        if c_num == '1':
            xm_id = input(u'请输入要获取的喜马拉雅节目的ID：')
            xima.get_fm(xm_id)
            self.index_choose()
        elif c_num == '2':
            xm_id = input(u'请输入要获取的音源：')
            print(xm_id)
            self.index_choose()
        elif c_num == '3':
            xm_id = input(u'请输入要获取的已付费的喜马拉雅节目的ID：')
            xima.get_pay_fm(xm_id)
            self.index_choose()
        elif c_num == '4':
            print('结束')
        else:
            pass

    @staticmethod
    def make_dir(xm_fm_id):
        # 保存路径，请自行修改，这里是以有声书ID作为文件夹的路径
        fm_path = 'F:\\{}\\'.format(xm_fm_id)
        f = os.path.exists(fm_path)
        if not f:
            os.makedirs(fm_path)
            print('make file success...')
        else:
            print('file already exists...')
        return fm_path

    def get_fm(self, xm_fm_id):
        # 根据有声书ID构造url
        fm_url = self.base_url + '/youshengshu/{}'.format(xm_fm_id)
        print(fm_url)
        r_fm_url = self.s.get(fm_url, headers=self.header)
        fm_title = re.findall('<h1 class="title _leU">(.*?)</h1>', r_fm_url.text, re.S)[0]
        print('书名：' + fm_title)
        # 新建有声书ID的文件夹
        fm_path = self.make_dir(xm_fm_id)
        # 取最大页数
        max_page = re.findall(r'<input type="number" placeholder="请输入页码" step="1" min="1" '
                              r'max="(\d+)" class="control-input _bfuk" value=""/>', r_fm_url.text, re.S)
        if max_page and max_page[0]:
            for page in range(1, int(max_page[0]) + 1):
                print('第' + str(page) + '页')
                self.get_sign()
                r = self.s.get(self.base_api.format(xm_fm_id, page), headers=self.header)
                # print(json.loads(r.text))
                r_json = json.loads(r.text)
                for audio in r_json['data']['tracksAudioPlay']:
                    audio_title = str(audio['trackName']).replace(' ', '')
                    audio_src = audio['src']
                    self.get_detail(audio_title, audio_src, fm_path)
                # 每爬取1页，30个音频，休眠3秒
                time.sleep(3)
        else:
            print(os.error)

    def get_pay_fm(self, xm_fm_id):
        # 根据有声书ID构造url
        fm_url = self.pay_api.format(xm_fm_id)
        print(fm_url)
        r_fm_url = self.s.get(fm_url, headers=self.header)
        r_json = r_fm_url.json()
        fm_title = r_json['data']['mainInfo']['albumTitle']
        # 取最大页数
        max_tracks = r_json['data']['tracksInfo']['trackTotalCount']
        max_page = math.ceil(int(r_json['data']['tracksInfo']['trackTotalCount'])/30)
        print('书名：' + fm_title)
        # 新建有声书ID的文件夹
        fm_path = self.make_dir(xm_fm_id)
        if max_tracks:
            r_album_alltracks = self.s.get(self.pay_api_allinfo.format(xm_fm_id, max_tracks), headers=self.header)
            raa_json = json.loads(r_album_alltracks.text)
            tracks = raa_json['data']['tracks']['list']
            for track in tracks:
                audio_id = track['trackId']
                audio_title = str(track['title']).replace(' ', '')
                audio_src = self.pay_api_single.format(audio_id)
                print(audio_title, audio_src)
                # self.get_detail(audio_title, audio_src, fm_path)
                # 每爬取1页，30个音频，休眠1~3秒
                time.sleep(random.randint(1, 3))
        else:
            print(os.error)

    def get_detail(self, title, src, path):
        r_audio_src = self.s.get(src, headers=self.header)
        m4a_path = path + title + '.m4a'
        if not os.path.exists(m4a_path):
            with open(m4a_path, 'wb') as f:
                f.write(r_audio_src.content)
                print(title + '保存完毕...')
        else:
            print(title + 'm4a已存在')


if __name__ == '__main__':
    xima = XiMa()
    xima.index_choose()
