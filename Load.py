import re
import time
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image




#——————————————————————————————————————
#模拟登陆
def analogLand(post_url,yzm_url):
    loginResults = 0
    while loginResults == 0:
        print('Loading-->')
        time.sleep(1)
        print('Loading-->')
        ID = input('Please Enter Your ID:')
        Password = input('Please Enter Your Password(Clear):')
        Code = ''
        logindata = {'zjh': ID, 'mm': Password, 'v_yzm': Code}
        session = requests.session()#建立会话，保持会话信息，cookies
        r = session.get(post_url)
        cookies = r.headers['Set-Cookie']  # 获取cookies
        cookies = cookies.strip('; path=/')  # 删除指定字符
        yam_headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'Host': '202.194.116.35',
            'Referer': 'http://202.194.116.35/loginAction.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
        }
        yamdata = session.get(yzm_url, headers=yam_headers)  # 获取验证码
        tempIm = BytesIO(yamdata.content)  # 将数据流放入tempIm以字节的形式
        im = Image.open(tempIm)  # 转换为图片的形式
        im.show()  # 展示验证码
        Code = input('Please Enter Code:')
        print('Loading-->')
        time.sleep(1)
        logindata['v_yzm'] = Code
        login_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '37',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '',
            'Host': '202.194.116.35',
            'Origin': 'http://202.194.116.35',
            'Referer': 'http://202.194.116.35/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
        }
        login_headers['Cookie'] = cookies
        d = session.post(post_url, data=logindata, headers=login_headers)
        verifyPassword(d)#验证密码是否正确
        loginResults = verifyLoginStatus(d)#验证登录状态
        print('——————————————————————')
    return session, cookies, ID

#————————————————————————————————————————————
#                           验证密码是否正确
def verifyPassword(html):
    html = BeautifulSoup(html.text, 'html.parser').findAll('strong')
    htmlMeg = str(html)
    if (htmlMeg == '[<strong><font color="#990000">用户名或密码不正确！</font></strong>]'):
        htmlMeg = re.findall('"#990000">' + '(.*?)' + '</font>', htmlMeg, re.S)
        print(htmlMeg)
    return

#————————————————————————————————————————————
#                           验证登录状态
def verifyLoginStatus(html):
    bs0bj = BeautifulSoup(html.text, 'html.parser').findAll('title')
    bs0bj = str(bs0bj)
    if bs0bj == '[<title>URP 综合教务系统 - 登录</title>]':
        loginResults = 0  # 连接失败
        print('Logon Failure')
        print('Reconnect In...')
    elif bs0bj == '[<title>学分制综合教务</title>]':
        loginResults = 1  # 连接成功
        print('Landing Success!')
    else:
        loginResults = 0
    return loginResults
