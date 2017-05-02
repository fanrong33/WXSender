# WXSender

## 为什么会有这个项目

微信公众号发送消息接口
因为需要认证，发送消息-客服接口	
公众号接口权限说明 https://mp.weixin.qq.com/wiki
公众号接口



WXSender 是用 Python 实现的微信公众平台微信发送接口，可以模拟在网页上登录微信公众平台，给指定或者所有好友发送微信。

WXSender 目前只支持纯文本消息的发送，可以作为一个消息群发器的接口，信息的数量每日不受限制。

# 用法

测试用例已经合成到 WXSender 类中，只需要如下代码即可测试：

'''python
wxs = WXSender()
wxs.run_test("abc@abc.com","abc")
'''

# cookie
# token
# user_fakeid


## 感激
感谢以下的项目

* [WXSender-Python](https://github.com/daoluan/WXSender-Python/) 
