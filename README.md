# WXSender
## 微信公众平台发送消息接口

因为需要认证，
WXSender 是用 Python 实现的微信公众平台微信发送接口，可以模拟在网页上登录微信公众平台，给指定或者所有好友发送微信。

WXSender 目前只支持纯文本消息的发送，可以作为一个消息群发器的接口，信息的数量每日不受限制。

# 用法

测试用例已经合成到 WXSender 类中，只需要如下代码即可测试：

'''python
wxs = WXSender()
wxs.run_test("abc@abc.com","abc")
'''