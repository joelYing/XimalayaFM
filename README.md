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

代码主要是通过`Scapy`实现的功能，对，`不是Scrapy`，Scapy具有模拟发送数据包、监听解析数据包、互联网协议解析、数据挖掘等多种用处  

然后发现scapy-http这个模块，二者配合使用后，可以解析抓到的包的url等参数  

### 安装工具
``` bash
pip3 install scapy

pip3 install scapy-http
```

还要安装winpcap软件，为监控网卡提供接口，[下载地址](https://www.winpcap.org/install/default.htm)  

注意替换代码中的iface：[iface 参数为你要监听的网卡的名称，参考这里](https://blog.csdn.net/luanpeng825485697/article/details/78379154)  

## Stargazers over time

[![Stargazers over time](https://starchart.cc/joelYing/XimalayaFM.svg)](https://starchart.cc/joelYing/XimalayaFM)
