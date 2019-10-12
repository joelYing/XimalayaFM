# XimalayaFM

python爬取喜马拉雅音频

## TODO

* 写一个UI界面  
* 提供多种爬取选项

## 更新

* 2019-10-12 19:10  

[CSDN](https://blog.csdn.net/weixin_42050513/article/details/101224552)上有人评论说`xm-sign`规则改了，于是去看了看，发现实际只改了一个字母，整体流程任可以看下方正文  
 
把`hashlib.md5("ximalaya-{}".format(servertime).encode()`中的`ximalaya`替换成`himalaya`即可  

改动点如下图

![](http://image.joelyings.com/20191012-1.png)

![](http://image.joelyings.com/20191012-2.png)

改动不大，可能是发现了有人在大量爬取，先小地方改动，随后可能会有较大的规则改动，教程写出来的目的是学习、测试，切勿过度爬取！  
