#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-5

import sys
import hashlib
import json
import math
import os
import random
import time
import requests
from scapy.layers.inet import TCP
from scapy.all import sniff
from scapy_http import http
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_XiMaDownloader(object):
    def setupUi(self, XiMaDownloader):
        XiMaDownloader.setObjectName("XiMaDownloader")
        XiMaDownloader.resize(600, 563)
        self.centralwidget = QtWidgets.QWidget(XiMaDownloader)
        self.centralwidget.setObjectName("centralwidget")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(20, 20, 191, 41))
        self.title_label.setLineWidth(1)
        self.title_label.setScaledContents(False)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setIndent(-1)
        self.title_label.setObjectName("title_label")
        self.verticalGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.verticalGroupBox.setGeometry(QtCore.QRect(0, 0, 601, 71))
        self.verticalGroupBox.setAutoFillBackground(True)
        self.verticalGroupBox.setStyleSheet("")
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.choose_label = QtWidgets.QLabel(self.centralwidget)
        self.choose_label.setGeometry(QtCore.QRect(10, 80, 201, 31))
        self.choose_label.setObjectName("choose_label")
        self.free_fm = QtWidgets.QCheckBox(self.centralwidget)
        self.free_fm.setGeometry(QtCore.QRect(20, 140, 91, 16))
        self.free_fm.setObjectName("free_fm")
        self.vip_fm = QtWidgets.QCheckBox(self.centralwidget)
        self.vip_fm.setGeometry(QtCore.QRect(150, 140, 111, 16))
        self.vip_fm.setObjectName("vip_fm")
        self.single_fm = QtWidgets.QCheckBox(self.centralwidget)
        self.single_fm.setGeometry(QtCore.QRect(290, 140, 71, 16))
        self.single_fm.setObjectName("single_fm")
        self.id_label = QtWidgets.QLabel(self.centralwidget)
        self.id_label.setGeometry(QtCore.QRect(20, 190, 171, 41))
        self.id_label.setObjectName("id_label")
        self.id_input_line = QtWidgets.QLineEdit(self.centralwidget)
        self.id_input_line.setGeometry(QtCore.QRect(200, 200, 133, 20))
        self.id_input_line.setObjectName("id_input_line")
        self.token_label = QtWidgets.QLabel(self.centralwidget)
        self.token_label.setGeometry(QtCore.QRect(20, 250, 161, 41))
        self.token_label.setObjectName("token_label")
        self.token_input_line = QtWidgets.QLineEdit(self.centralwidget)
        self.token_input_line.setGeometry(QtCore.QRect(200, 260, 361, 20))
        self.token_input_line.setObjectName("token_input_line")
        self.d_type_box = QtWidgets.QGroupBox(self.centralwidget)
        self.d_type_box.setGeometry(QtCore.QRect(10, 120, 581, 51))
        self.d_type_box.setObjectName("d_type_box")
        self.path_input_line = QtWidgets.QLineEdit(self.centralwidget)
        self.path_input_line.setGeometry(QtCore.QRect(200, 230, 133, 20))
        self.path_input_line.setObjectName("path_input_line")
        self.path_label = QtWidgets.QLabel(self.centralwidget)
        self.path_label.setGeometry(QtCore.QRect(20, 220, 171, 41))
        self.path_label.setObjectName("path_label")
        self.d_config_box = QtWidgets.QGroupBox(self.centralwidget)
        self.d_config_box.setGeometry(QtCore.QRect(10, 180, 581, 111))
        self.d_config_box.setObjectName("d_config_box")
        self.choose_file_button = QtWidgets.QPushButton(self.d_config_box)
        self.choose_file_button.setGeometry(QtCore.QRect(340, 50, 75, 23))
        self.choose_file_button.setObjectName("choose_file_button")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(510, 320, 75, 23))
        self.run_button.setObjectName("run_button")
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(510, 360, 75, 23))
        self.cancel_button.setObjectName("cancel_button")
        self.output_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.output_text.setGeometry(QtCore.QRect(10, 300, 491, 241))
        self.output_text.setObjectName("output_text")
        self.d_config_box.raise_()
        self.d_type_box.raise_()
        self.verticalGroupBox.raise_()
        self.title_label.raise_()
        self.choose_label.raise_()
        self.free_fm.raise_()
        self.vip_fm.raise_()
        self.single_fm.raise_()
        self.id_label.raise_()
        self.id_input_line.raise_()
        self.token_label.raise_()
        self.token_input_line.raise_()
        self.path_input_line.raise_()
        self.path_label.raise_()
        self.run_button.raise_()
        self.cancel_button.raise_()
        self.output_text.raise_()
        XiMaDownloader.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(XiMaDownloader)
        self.statusbar.setObjectName("statusbar")
        XiMaDownloader.setStatusBar(self.statusbar)

        self.retranslateUi(XiMaDownloader)
        self.cancel_button.clicked.connect(XiMaDownloader.close)
        QtCore.QMetaObject.connectSlotsByName(XiMaDownloader)

    def retranslateUi(self, XiMaDownloader):
        _translate = QtCore.QCoreApplication.translate
        XiMaDownloader.setWindowTitle(_translate("XiMaDownloader", "XiMaFM下载器"))
        self.title_label.setText(_translate("XiMaDownloader", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">XiMaFM下载器</span></p></body></html>"))
        self.choose_label.setText(_translate("XiMaDownloader", "<html><head/><body><p><span style=\" font-size:11pt;\">请选择需要下载的音频类型：</span></p></body></html>"))
        self.free_fm.setText(_translate("XiMaDownloader", "免费有声书"))
        self.vip_fm.setText(_translate("XiMaDownloader", "VIP/付费有声书"))
        self.single_fm.setText(_translate("XiMaDownloader", "单个音频"))
        self.id_label.setText(_translate("XiMaDownloader", "<html><head/><body><p><span style=\" font-size:10pt;\">请输入需要下载的音频ID：</span></p></body></html>"))
        self.token_label.setText(_translate("XiMaDownloader", "<html><head/><body><p><span style=\" font-size:10pt;\">请输入你的会员token：</span></p></body></html>"))
        self.d_type_box.setTitle(_translate("XiMaDownloader", "下载类型"))
        self.path_label.setText(_translate("XiMaDownloader", "<html><head/><body><p><span style=\" font-size:10pt;\">请输入保存文件的路径：</span></p></body></html>"))
        self.d_config_box.setTitle(_translate("XiMaDownloader", "下载配置"))
        self.choose_file_button.setText(_translate("XiMaDownloader", "选择文件夹"))
        self.run_button.setText(_translate("XiMaDownloader", "运行"))
        self.cancel_button.setText(_translate("XiMaDownloader", "取消"))


class XiMaControl(QMainWindow, Ui_XiMaDownloader):
    def __init__(self):
        super(XiMaControl, self).__init__()
        self.setupUi(self)
        self.choose_file_button.clicked.connect(self.open_folder)
        self.free_fm.clicked.connect(self.free_check_box)
        self.vip_fm.clicked.connect(self.vip_check_box)
        self.single_fm.clicked.connect(self.single_check_box)
        self.run_button.clicked.connect(self.run)
        self.info = 0
        self.ximamain = XiMaMain()

    def open_folder(self):
        # 选取文件
        foldername = QFileDialog.getExistingDirectory(self, "选择文件夹", "F:/")
        foldername = str(foldername).replace('/', '\\')
        # print(foldername)
        self.path_input_line.setText(foldername)

    def free_check_box(self):
        if self.free_fm.isChecked() and self.vip_fm.isChecked() is False and self.single_fm.isChecked() is False:
            self.info = 1

    def vip_check_box(self):
        if self.vip_fm.isChecked() and self.free_fm.isChecked() is False and self.single_fm.isChecked() is False:
            self.info = 2

    def single_check_box(self):
        if self.single_fm.isChecked() and self.vip_fm.isChecked() is False and self.free_fm.isChecked() is False:
            self.info = 3

    def run(self):
        try:
            xm_id = self.id_input_line.text()
            folder_path = self.path_input_line.text()
            token = self.token_input_line.text()
            # message = str(self.info) + xm_id + folder_path + token
            # print_text(message)
            if self.info == 1:
                self.ximamain.get_free_fm(xm_id, folder_path)
            elif self.info == 2:
                self.ximamain.get_pay_fm(xm_id, folder_path, token)
            elif self.info == 3:
                print_text(xm_id)
            else:
                pass
        except Exception as e:
            print(e)


class XiMa:
    def __init__(self):
        self.base_url = 'https://www.ximalaya.com'
        # 有声书
        self.yss_api = 'https://www.ximalaya.com/youshengshu/{}/{}'
        # 需要带上sign访问的api，适用于免费的音频的播放源
        self.free_sign_api = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort=0&pageSize=30'
        # 获取单个免费音频api （trackId）
        self.free_track_api = 'http://mobile.ximalaya.com/mobile/redirect/free/play/{}/2'
        # 时间戳api
        self.time_api = 'https://www.ximalaya.com/revision/time'
        # 获取节目总音源个数与节目名
        self.album_api = 'https://www.ximalaya.com/revision/album?albumId={}'
        # 获取指定albumID的每一页音频的ID等track信息
        self.album_tracks_api = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'
        # APP抓包得到，可用于获取付费节目总音源个数与节目名，获取音集所有音频ID，通过改变pageSize的大小，（albumId, pageSize）
        # 2020-02-29 最新测试pageSize最大为1000，所以针对章节大的有声书修改规则
        self.pay_size_api = 'http://180.153.255.6/mobile-album/album/page/ts-1569206246849?ac=WIFI&albumId={}' \
                            '&device=android&isAsc=true&isQueryInvitationBrand=true&isVideoAsc=true&pageId=1' \
                            '&pageSize={}'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
        self.s = requests.session()

    def get_time(self):
        """
        获取服务器时间戳
        """
        r = self.s.get(self.time_api, headers=self.header)
        r_time = r.text
        return r_time

    def get_sign(self):
        """
        获取sign： md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        """
        nowtime = str(round(time.time() * 1000))
        servertime = self.get_time()
        sign = str(hashlib.md5("himalaya-{}".format(servertime).encode()).hexdigest()) + "({})".format(
            str(round(random.random() * 100))) + servertime + "({})".format(str(round(random.random() * 100))) + nowtime
        self.header["xm-sign"] = sign

    def make_dir(self, xm_fm_id, path):
        """
        保存路径，请自行修改，这里是以有声书ID作为文件夹的路径
        """
        fm_path = path + '\\' + xm_fm_id
        if str(path).endswith('\\'):
            fm_path = path + xm_fm_id
        f = os.path.exists(fm_path)
        if not f:
            os.makedirs(fm_path)
            print_text('make file success...')
        else:
            print_text('file already exists...')
        return fm_path

    def get_fm(self, xm_fm_id, path):
        """
        根据albumID解析 免费 fm信息
        """
        # 根据有声书ID构造url
        r_fm_url = self.s.get(self.album_api.format(xm_fm_id), headers=self.header)
        r_fm_json = json.loads(r_fm_url.text)
        fm_title = r_fm_json['data']['mainInfo']['albumTitle']
        fm_count = r_fm_json['data']['tracksInfo']['trackTotalCount']
        fm_page_size = r_fm_json['data']['tracksInfo']['pageSize']
        print_text('书名：' + fm_title)
        # 新建有声书ID的文件夹
        fm_path = self.make_dir(xm_fm_id, path)
        # 取最大页数，向上取整
        max_page = math.ceil(fm_count/fm_page_size)
        return fm_count, fm_path, max_page

    def get_free_sign(self, xm_fm_id, page):
        """
        下载免费的音频的播放源信息
        :param xm_fm_id:
        :param page:
        :return: response
        """
        self.get_sign()
        response = self.s.get(self.free_sign_api.format(xm_fm_id, page), headers=self.header)
        return response

    def get_pay_album(self, xm_fm_id, page_num):
        """
        获取付费的音频的播放源信息
        :param xm_fm_id:
        :param max_page:
        :return: response
        """
        response = self.s.get(self.album_tracks_api.format(xm_fm_id, page_num), headers=self.header)
        return response

    def save_fm2local(self, title, src, path):
        """
        保存音频到本地
        :param title:
        :param src:
        :param path:
        """
        r_audio_src = requests.get(src, headers=self.header)
        m4a_path = path + '\\' + title + '.m4a'
        if not os.path.exists(m4a_path):
            with open(m4a_path, 'wb') as f:
                f.write(r_audio_src.content)
                print_text(title + '保存完毕...')
        else:
            print_text(title + '.m4a 已存在')


class XiMaMain:
    def __init__(self):
        self.xmd = XiMa()

    def get_free_fm(self, xm_fm_id, path):
        fm_count, fm_path, max_page = self.xmd.get_fm(xm_fm_id, path)
        if max_page:
            for page in range(1, int(max_page) + 1):
                print_text(str('第' + str(page) + '页'))
                r = self.xmd.get_free_sign(xm_fm_id, page)
                r_json = json.loads(r.text)
                for audio in r_json['data']['tracksAudioPlay']:
                    audio_title = str(audio['trackName']).replace(' ', '')
                    audio_src = audio['src']
                    self.xmd.save_fm2local(audio_title, audio_src, fm_path)
                # 每爬取1页，30个音频，休眠3秒
                time.sleep(3)
        else:
            print_text('no max_page')

    def get_pay_fm(self, xm_fm_id, path, token):
        fm_count, fm_path, max_page = self.xmd.get_fm(xm_fm_id, path)
        if max_page:
            # 这里应该是 fm_count
            for p in range(1, int(max_page) + 1):
                r = self.xmd.get_pay_album(xm_fm_id, p)
                r_json = json.loads(r.text)
                tracks = r_json['data']['tracks']
                for i, track in enumerate(tracks):
                    audio_id = track['trackId']
                    audio_title = str(track['title']).replace(' ', '')
                    audio_url = self.xmd.base_url + track['url']
                    print_text(str(audio_title + '' + audio_url))
                    real_url = self.auto_click(audio_url, token)
                    self.xmd.save_fm2local(audio_title, real_url, fm_path)
                    # 每爬取1页，30个音频，休眠1~3秒
                    time.sleep(random.randint(1, 3))
        else:
            print_text('no max_page')

    def auto_click(self, url, token):
        """
        参数url为对应的VIP音频的播放页面，selenium访问页面后，带上cookie（1&_token）模拟登陆再次访问，前提你已经是会员
        等待页面加载完成，通过selenium+Chromedriver的无头浏览器模拟点击音频播放按钮
        scapy开始抓点击后音频真实地址的数据包，退出browser，解析包
        注意click与抓包的顺序，先点击再抓包
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(url)
        browser.add_cookie({
            # 此处xxx.com前，需要带点，注意domain也是cookie必须的
            'domain': '.ximalaya.com',
            'name': '1&_token',
            'value': token,
        })
        browser.get(url)
        time.sleep(4)
        print_text('开始抓包')
        # selenium 点击播放按钮
        browser.find_element_by_css_selector(".play-btn.fR_").click()
        # 下面的iface是电脑网卡的名称 count是捕获报文的数目
        pkts = sniff(filter="tcp and port 80", iface="Qualcomm Atheros AR956x Wireless Network Adapter", count=5)
        browser.quit()
        for pkt in pkts:
            if TCP in pkt and pkt.haslayer(http.HTTPRequest):
                http_header = pkt[http.HTTPRequest].fields
                req_url = 'http://' + bytes.decode(http_header['Host']) + bytes.decode(http_header['Path'])
                return req_url


def print_text(msg):
    control.output_text.append(msg)
    print(msg)
    QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    control = XiMaControl()
    control.show()
    sys.exit(app.exec_())

