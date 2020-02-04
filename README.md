# XimalayaFM

python爬取喜马拉雅音频

## TODO

* 写一个UI界面  
* 提供多种爬取选项

## 2019-10-12 19:10 

[CSDN](https://blog.csdn.net/weixin_42050513/article/details/101224552)上有人评论说`xm-sign`规则改了，于是去看了看，发现实际只改了一个字母，整体流程任可以看下方正文  
 
把`hashlib.md5("ximalaya-{}".format(servertime).encode()`中的`ximalaya`替换成`himalaya`即可  

改动点如下图

![](http://image.joelyings.com/20191012-1.png)

![](http://image.joelyings.com/20191012-2.png)

改动不大，可能是发现了有人在大量爬取，先小地方改动，随后可能会有较大的规则改动，教程写出来的目的是学习、测试，切勿过度爬取！  

## 2020-02-02

完成VIP音频下载功能  

使用方法：  

* 首先你已经开通了喜马会员   
* 该音频属于会员或者付费可听  
* 运行程序，选择`VIP`选项，然后输入音频集的albumID，以及你的token，点击运行即可  

token在下图这里复制  

![](http://image.joelyings.com/2020-02-02_1.png)

就是`1&_token=xxx`，这一部分，不用加`;`  

### 探索过程

这次为了《雪中》付费的下半部，我再次尝试下载音频，通过一个活动领取了15天的免费喜马VIP  

然后打开下半部的[页面](https://www.ximalaya.com/youshengshu/5130435/)  

这里只有前三个音频是`试听`的，也就是说前三个是我们可以在不开通VIP的情况下也可以下载的，但是后面的就不行，幸好现在开了VIP都可以收听  

对`第861回`这个收费音频来分析，页面加载完成后，打开`fiddler`抓包，观察点击播放按钮后抓到的数据包  

我们可以发现两个链接：  

```
# 链接一
https://mpay.ximalaya.com/mobile/track/pay/20641515?device=pc&isBackend=true&_=1580528471441

# 返回的response
ret: 0,
msg: "0",
trackId: 20641515,
uid: 2342717,
albumId: 5130435,
title: "雪中悍刀行 - 861",
domain: "http://audiopay.cos.xmcdn.com",
totalLength: 10533707,
sampleDuration: 0,
sampleLength: 0,
isAuthorized: true,
apiVersion: "1.0.0",
seed: 8644,
fileId: "6*33*22*66*59*29*62*11*31*3*62*67*47*62*31*29*62*54*21*6*63*11*52*48*50*52*41*38*1*23*33*51*30*28*21*45*43*51*54*1*48*66*6*22*34*3*34*15*5*3*46*",
buyKey: "617574686f72697a6564",
duration: 1301,
ep: "20NvOoh6T39X3qwKO4cY5g5bVhg+hSXHRYUYeFznDiuuzOiKiKrbmelc2/zZg6UxDO9x2nIYeKZm0+z+xg0V3r0aPyxS",
highestQualityLevel: 1,
downloadQualityLevel: 1,
authorizedType: 1
```

```
# 链接二 没有返回，这就是音频的真实播放地址

http://audiopay.cos.xmcdn.com/download/1.0.0/group1/M04/DF/01/wKgJMlvblh6xqrSXAKC7Swxvugo848.m4a?sign=a464311c1753bfdf581ac9560dc8bf9a&buy_key=617574686f72697a6564&token=5400&timestamp=1580528473&duration=1301
```

链接二携带的参数  

| 参数 | 值 | 状态 |
|--|--|--|
|sign|a464311c1753bfdf581ac9560dc8bf9a|变化|
|buy_key|617574686f72697a6564|固定|
|token|5400|变化|
|timestamp|1580528473|时间戳|
|duration|1301|每个音频特有|

链接二的`M04/DF/01/wKgJMlvblh6xqrSXAKC7Swxvugo848`也是变化的  

问题就在于链接一我们很好理解，带上音频的ID就可以返回一串response，再通过JS生成链接二得到音频真实地址  

关键在于这个JS比较麻烦，JS片段：  

``` javascript
var gt = vt("xm", "Ä[ÜJ=Û3Áf÷N")
  , bt = [19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35, 34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18, 3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26]
  , wt = function(t) {
    var e = vt(function(t, e) {
        for (var n = [], r = 0; r < t.length; r++) {
            for (var o = "a" <= t[r] && "z" >= t[r] ? t[r].charCodeAt() - 97 : t[r].charCodeAt() - "0".charCodeAt() + 26, i = 0; 36 > i; i++)
                if (e[i] == o) {
                    o = i;
                    break
                }
            n[r] = 25 < o ? String.fromCharCode(o - 26 + "0".charCodeAt()) : String.fromCharCode(o + 97)
        }
        return n.join("")
    }("d" + gt + "9", bt), function(t) {
        if (!t)
            return "";
        var e, n, r, o, i, a = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1];
        for (o = (t = t.toString()).length,
        r = 0,
        i = ""; r < o; ) {
            do {
                e = a[255 & t.charCodeAt(r++)]
            } while (r < o && -1 == e);if (-1 == e)
                break;
            do {
                n = a[255 & t.charCodeAt(r++)]
            } while (r < o && -1 == n);if (-1 == n)
                break;
            i += String.fromCharCode(e << 2 | (48 & n) >> 4);
            do {
                if (61 == (e = 255 & t.charCodeAt(r++)))
                    return i;
                e = a[e]
            } while (r < o && -1 == e);if (-1 == e)
                break;
            i += String.fromCharCode((15 & n) << 4 | (60 & e) >> 2);
            do {
                if (61 == (n = 255 & t.charCodeAt(r++)))
                    return i;
                n = a[n]
            } while (r < o && -1 == n);if (-1 == n)
                break;
            i += String.fromCharCode((3 & e) << 6 | n)
        }
        return i
    }(t)).split("-")
      , n = tt(e, 4)
      , r = n[0];
    return {
        sign: n[1],
        buy_key: r,
        token: n[2],
        timestamp: n[3]
    }
}
```

还有加密的字符`var gt = vt("xm", "Ä[ÜJ=Û3Áf÷N")`，全部代码在[这里](http://image.joelyings.com/b20b549ee.js)  

有能力的各位可以试着解决一下哈哈~  

鉴于本人JS能力不够便放弃了这种方法，但是又想到`只要获取这个链接二就可以下载音频`，那么我能不能`直接拿到这个链接`而不是通过JS生成一系列相关的参数去构造  

随后我就想到了抓包，我们通过fiddler可以抓到这个链接，那么，Python有没有类似的第三方库呢？  

答案是有的，`Scapy`，对，`不是Scrapy`，Scapy具有模拟发送数据包、监听解析数据包、互联网协议解析、数据挖掘等多种用处  

然后发现scapy-http这个模块，二者配合使用后，可以解析抓到的包的url等参数  

### 安装工具
``` bash
pip3 install scapy

pip3 install scapy-http
```

还要安装winpcap软件，为监控网卡提供接口，[下载地址](https://www.winpcap.org/install/default.htm)  

[iface 参数为你要监听的网卡的名称，参考这里](https://blog.csdn.net/luanpeng825485697/article/details/78379154)  

``` python
# 核心代码，因为观察到链接二，这个音频真实链接的发送IP是变化的，但是端口是固定的80
# count=5，表示抓取5个端口为80且属于TCP的报文
# 在对应的音频详情播放页，运行程序后，点击播放按钮，然后就可以抓到，注意顺序不能乱

pkts = sniff(filter="tcp and port 80", iface="Qualcomm Atheros AR956x Wireless Network Adapter", count=5)
print('抓包成功,开始解析', pkts)
for pkt in pkts:
    # 判断是否有HTTPRequest
    if TCP in pkt and pkt.haslayer(http.HTTPRequest):
        # print(pkt.show())
        http_header = pkt[http.HTTPRequest].fields
        req_url = 'http://' + bytes.decode(http_header['Host']) + bytes.decode(http_header['Path'])
        # print(req_url)
        return req_url
```

```
# ptk.show()的内容示例

###[ Ethernet ]### 
  ...
  type      = IPv4
###[ IP ]### 
     ...
     \options   \
###[ TCP ]### 
        ...
        options   = []
###[ HTTP ]### 
###[ HTTP Request ]### 
      Method    = 'GET'
      Path      = '/download/1.0.0/group1/M02/DE/F7/wKgJMlvbkluA76b0AKfFEVJys4k253.m4a?sign=68fbb62e424b3af077c30a9a2d4e8bad&buy_key=617574686f72697a6564&token=4060&timestamp=1580616979&duration=1358'
      Http-Version= 'HTTP/1.1'
      Host      = 'audiopay.cos.xmcdn.com'

      ...

      Headers   = 'Host: audiopay.cos.xmcdn.com\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/79.0.3945.130 Safari/537.36\r\nAccept-Encoding: identity;q=1, *;q=0\r\nAccept: */*\r\nRange: bytes=0-'
      Additional-Headers= None

```

这样我们就可以通过抓包的方式直接拿到链接，但是要一个一个点播放按钮还是太耗人力，所辛我们还有`selenium`+`Chromedriver`  

可以设置Chromedriver为headless模式  

``` python
# 设置无头模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)
# 访问音频播放页面，这是为了后面添加cookie指定添加的页面是哪一个
browser.get(url)
# 添加cookie
browser.add_cookie({
    'domain': '.ximalaya.com',  # 此处xxx.com前，需要带点
    'name': '1&_token',
    'value': 'xxx'
})
# 添加cookie后的再次访问
browser.get(url)
# 等待加载页面完全
time.sleep(4)
print('开始抓包')
# 点击播放按钮，这里的顺序不能搞错，换成先抓包再点击的话，试过，但是抓不到
browser.find_element_by_css_selector(".play-btn.fR_").click()
# 下面的iface是电脑网卡的名称 count是捕获报文的数目
pkts = sniff(filter="tcp and port 80", iface="Qualcomm Atheros AR956x Wireless Network Adapter", count=5)
print('抓包成功,开始解析', pkts)
# 退出browser，避免selenium报错
browser.quit()

...

```

