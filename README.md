# WXSender
WXSender 是用 Python 实现的微信公众平台微信发送接口，可以模拟在网页上登录微信公众平台，给指定好友发送微信。

WXSender 目前只支持纯文本消息的发送，可以作为一个消息发送的接口，信息的数量每日不受限制。

## Overview

因为一个项目的需求，想要使用微信公众号来作为交互的界面，以被动模式来通知自己，所以需要使用微信公众号的发送消息-客服接口，具体可见[公众号接口权限说明](https://mp.weixin.qq.com/wiki)。但悲催的是微信公众号需要进行认证（每年300软妹币），才有接口权限。所以只能自己模拟登录网页版后台了😞


## Usage

测试用例已经合成到 WXSender 类中，只需要如下代码即可测试：

```python
from wxsender import WXSender

wxsender = WXSender()
wxsender.send_message(touser='oyAU3v3oDtr00EPuFUUxylEYHezg', msgtype='text', text={'content':'Hello Wechat'})
```

## Install

* cookie
* token
* user_fakeid


### Thanks
感谢以下的项目

* [WXSender-Python](https://github.com/daoluan/WXSender-Python/) 
