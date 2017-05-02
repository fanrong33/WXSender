# encoding: utf-8
# @author 蔡繁荣
# @version 1.0.0 build 20170502
# @environment Python 2.7
# 需要注意的地方是：微信公众平台要求如果你的粉丝在 48 小时内没有与公众账号联系过，微信公众账号就无法主动发信息给你的粉丝

import urllib2,cookielib,re
import json
import hashlib
import sys

# fix encoding bug
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



def goodboy(funcname):
    print("%s finished." % funcname)


class WXSender:
    
    '''
        登录->获取微信公众账号 fakeid->获取好友 fakeid->向所有好友群发送微信或者向指定好友发送微信
        其中 fakeid 是在网页版微信中用到的参数，可以看作是用户的标识
        
        `登录过程中，主要是记录 cookie，在之后的通信中都要往 HTTP header 中添加 cookie，否则微信会作「登陆超时」处理，微信后台应该
            是用此 cookie 来作 session 的；另，在返回的 json 中有 token 参数，也需要记录，具体作用还不明，但发现一个现象：当下
            修改 token 为其他值不影响操作，但隔一天使用前一天的 token 则无效
        `获取的好友 fakeid 全在返回页面的 json 中
        `聊天，用 fiddler 抓包，所以手上三件东西就可以聊天了：cookie，fromfakeid 和 tofakeid
    '''
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    
    # TODO 暂时先手动设置
    wx_cookie   = ''
    token       = ''
    user_fakeid = ''

    friend_info = []        # 好友 fakeid
    
    # def __init__(self):
    #     pass
    
    ''' 模拟登录方法
    该接口已失效，因为微信公众账号要求必须运营人员扫描二维码才可登录
    不过不失为一个模拟登录的参考示例
    策略：手动设置 wx_cookie 和 token 属性，在扫描二维码登录成功后，通过开发者工具组装成类似 document.cookie 的格式
    '''
    def login(self,account,pwd):

        # 获取 cookie
        cookies = cookielib.LWPCookieJar()
        cookie_support= urllib2.HTTPCookieProcessor(cookies)
        
        # bulid a new opener
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
        pwd = hashlib.md5(pwd).hexdigest()
        req = urllib2.Request(url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN',
                              data = ('username=' + account + 
                              '&pwd=' + pwd + 
                              '&imgcode='
                              '&f=json'))
        
        req.add_header("x-requested-with", "XMLHttpRequest")
        req.add_header("referer", "https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN")
        response = opener.open(req).read()
        response_json = json.loads(response)
        
        if response_json['ErrCode'] < 0:
            raise Exception("Login error.")
        
        s = re.search(r'token=(\d+)', response_json['ErrMsg'])
        
        if not s:
            raise Exception("Login error.")
        
        self.token = s.group(1)
        
        for cookie in cookies:
            self.wx_cookie += cookie.name + '=' + cookie.value + ';'
        # print 'wx_cookie ',self.wx_cookie
        # print 'token ',self.token
        
        goodboy(self.login.__name__)
        

    ''' 获取微信公众账号的fakeid
    未使用
    '''
    def get_fakeid(self):

        self.wx_cookie = 'cert=v4VFx8MS6K8Jkw5PAhnyikfm1vffgvSM; data_bizuin=3012015708; data_ticket=L++FG2UF8fS/LjEIQd701H0qEISiFnVIhJ3k2dpCeO2js6lVHBUTxC9tczIoU+23; noticeLoginFlag=0; openid2ticket_oXLaHs5D7NAgg-FbELIkpBpIbYJE=nahbK1a4PJmaQZx+/meG4YPW8eRQG6CyTETm7ELvQJE=; account=modougame@qq.com; bizuin=2395316436; slave_sid=R09Nd3dNcm5UWVNOQjdPdGxsOW00eUpCRXZ5cE9QbWdsZXRqR1hGcFN6VmJFOW9RSEtKbmV6UEFIT2xwcmQwOEdBTk9sRjV6UThUbVNDQU9JNExsN1BNTjlmdjVvU3gzbVZ0dnJhcEVXdVB1NUxKSnNJYW1jSHF2YzlqREg4SlVSTjRvYURiNWhuS25wT3NZ; slave_user=gh_f44acd30e500; ticket=c83749d71ae903f2c6898ce035b6511184cd19f2; ticket_id=gh_f44acd30e500; ua_id=90TEYuChla8fxxYzAAAAAH-oVr3a9mHV1SogWXo9ErE=; uuid=0e9f0d792735cdb047bd8c0d3eb042e3; xid=e40a11b296b523db85bc14af059be789'
        self.token = '541021219'
        self.user_fakeid = 2395316436

        if not (self.wx_cookie and self.token):
            raise Exception("Cookies or token is missing.")
        
        url = 'https://mp.weixin.qq.com/cgi-bin/settingpage?t=setting/index&action=index&token=' + self.token + '&lang=zh_CN'
        req = urllib2.Request(url, headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
        req.add_header('cookie', self.wx_cookie)
        
        data = urllib2.urlopen(req,timeout = 4).read()

        m = re.search(r'fakeid=(\d+)',data,re.S | re.I)
        
        # group(0) == [fakeid = "123456789"]
        if not m:
            raise Exception("Getting fakeid failed.")
        
        self.user_fakeid = m.group(1)


        print(self.user_fakeid)
        goodboy(self.get_fakeid.__name__)
        
    ''' 获取微信公众账号的粉丝fakeid
    未使用
    '''
    def get_friend_fakeid(self):
        if not (self.wx_cookie and self.token and self.user_fakeid):
            raise Exception("Cookies,token or user_fakeid is missing.")
        
        # 获取 friend fakeid
        base_url = ('https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&lang=zh_CN&pagesize=50' + 
                    '&type=0&groupid=0' + 
                    '&token=' + self.token + 
                    '&pageidx=')    # pageidx = ?
        
        # 这里可以根据微信好友的数量调整，由 base_url 可知一页可以显示 pagesize = 50 人，看实际情况吧。
        for page_idx in xrange(0,1000):
        
            url = base_url + str(page_idx)
            req = urllib2.Request(url)
            req.add_header('cookie',self.wx_cookie)
            data = urllib2.urlopen(req).read()  
            p = re.compile(r'"id":([0-9]{4,20})')
            res = p.findall(data)
            
            if not res:
                break
            
            for id in res:
                self.friend_info.append({"id":id})

        goodboy(self.get_friend_fakeid.__name__)
        

    ''' 群发接口：目前只支持发送文本信息 
    "touser":"OPENID",
    "msgtype":"text",
    "text":{ "content":"Hello World" }
    '''
    def send_message(self, touser, msgtype='text', text={}):

        if not (self.wx_cookie and self.token and self.user_fakeid):
            raise Exception("Cookies,token,user_fakeid or friend_info is missing.")
        

        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&lang=zh_CN'
        post_data = ('type=1&content=%s&error=false&imgcode=&token=%s&ajax=1&tofakeid=%s') % (text['content'], self.token, touser)   # fakeid = ?

        request = urllib2.Request(url, post_data, headers = { 'User-Agent': self.user_agent})
        request.add_header('cookie', self.wx_cookie)
        
        # 添加 HTTP header 里的 referer 欺骗腾讯服务器。如果没有此 HTTP header，将得到登录超时的错误。
        request.add_header('referer', ('https://mp.weixin.qq.com/cgi-bin/singlemsgpage?'
                               'token=%s&fromfakeid=%s'
                               '&msgid=&source=&count=20&t=wxm-singlechat&lang=zh_CN') % (self.token, self.user_fakeid))
        
        res = urllib2.urlopen(request).read()
        # print(res)
        # {"base_resp":{"err_msg":"","ret":0}}

        res_json = json.loads(res)
        if res_json['base_resp']["ret"] != "0":
            # do something.
            pass
            
        goodboy(self.send_message.__name__)
        

    def run(self, account, pwd):
        # 登录，需要提供正确的账号密码
        # self.login(account, pwd)
        
        # 获取微信公众账号 fakeid
        # self.get_fakeid()
        
        # 获取微信好友的所有 fakeid，保存再 self.friend_info 中
        # self.get_friend_fakeid()
        
        # 群发接口：目前只能发送文本信息
        self.group_sender("Hello World[鸡]")
        

if __name__ == '__main__':
    # 使用方法
    wxsender = WXSender()

    wxsender.send_message(touser='oyAU3v3oDtr00EPuFUUxylEYHezg', msgtype='text', text={'content':'Hello World[鸡]'})



