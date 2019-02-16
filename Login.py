# !/usr//bin/env python3
# -*- coding: utf-8 -*-

import requests
import Ocr
import time
from Common import jsonData, setHeaders


class Login():
    # 初始化类
    def __init__(self, username, password):
        self.headers = setHeaders()
        self.data = {
            'j_username': username,
            'j_password': password,
            'username': '',
            'password': '',
            'j_captcha': '',
            'login': '登录'
        }
        self.url = {
            'login': 'http://jw.qdu.edu.cn/academic/common/security/login.jsp',
            'captcha': 'http://jw.qdu.edu.cn/academic/getCaptcha.do',
            'post': 'http://jw.qdu.edu.cn/academic/j_acegi_security_check',
            'check': 'http://jw.qdu.edu.cn/academic/checkCaptcha.do',
        }
        self.r = requests.Session()

    # 下载验证码
    def down_captcha(self):
        # 先请求login，获取下cookie
        self.r.get(url=self.url['login'], headers=self.headers)
        pic = self.r.get(url=self.url['captcha'], headers=self.headers)
        return pic.content

    # 识别验证码
    def ocr_captcha(self):
        content = self.down_captcha()
        code = Ocr.ocr_api(content)
        count = 0
        while code == False:
            time.sleep(1)
            if (count > 15):
                print('识别上传错误')
                return False
            count += 1
            code = Ocr.ocr_api(content)
        return code.replace(' ', '')  # 去除空格

    # 校验验证码
    def check_captcha(self, code):
        check = self.r.get(url=self.url['check'], headers=self.headers, params={
                           'captchaCode': code})
        # 调用接口，判断验证码是否正确
        if (check.json() == False):
            return False
        self.data['j_captcha'] = code
        return True

    # 登陆
    def to_login(self):
        code = self.ocr_captcha()
        count = 0
        while self.check_captcha(code) == False:
            if (count > 10):
                return jsonData(400, False, '验证码识别错误，请稍后重试')
            code = self.ocr_captcha()
            count += 1
        res = self.r.post(
            url=self.url['post'], headers=self.headers, data=self.data,)
        # 登陆成功会重定向到此url
        if (res.url != 'http://jw.qdu.edu.cn/academic/index_new.jsp'):
            print(self.data)
            print('账号密码错误')
            return jsonData(400, False, '账号密码错误！请核对后重试')
        return jsonData(200, self.r.cookies['JSESSIONID'], '登陆成功')
