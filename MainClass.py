# !/usr//bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
import pymysql
import pymysql.cursors
import Ocr
import time
import json


class Login():
    # 初始化类
    def __init__(self, username, password, cookie=None, uid=None):
        self.headers = {
            'Host': 'jw.qdu.edu.cn',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
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
            'schedule': 'http://jw.qdu.edu.cn/academic/manager/coursearrange/showTimetable.do'
        }
        self.r = requests.Session()
        self.cookies = {'JSESSIONID': cookie}
        self.uid = uid

    # 下载验证码

    def down_captcha(self):
        # 先请求login，获取下cookie
        self.r.get(url=self.url['login'], headers=self.headers)
        pic = self.r.get(url=self.url['captcha'], headers=self.headers)
        # with open('code.jpg', 'wb') as f:
        #     f.write(pic.content)
        return pic.content

    # 登陆
    def to_login(self):
        # 假如cookie不为空，就用cookie登陆
        if (self.cookies['JSESSIONID'] != None):
            print('cookie登陆')
            requests.utils.add_dict_to_cookiejar(self.r.cookies, self.cookies)
            return True

        # code = input('请输入验证码：')
        code = self.ocr_captcha()
        count = 0
        while self.check_captcha(code) == False:
            if (count > 10):
                print('验证码识别错误，退出')
                return False
            code = self.ocr_captcha()
            count += 1
        res = self.r.post(
            url=self.url['post'], headers=self.headers, data=self.data,)
        # 登陆成功会重定向到此url
        if (res.url != 'http://jw.qdu.edu.cn/academic/index_new.jsp'):
            print('账号密码错误')
            return False
        print('登陆成功')
        print(self.r.cookies['JSESSIONID'])
        self.insert_cookie()
        return True

    # 识别验证码
    def ocr_captcha(self):
        content = self.down_captcha()
        code = Ocr.ocr_api(content)
        count = 0
        while code == False:
            time.sleep(550)
            if (count > 15):
                print('识别上传错误')
                return False
            count += 1
            code = Ocr.ocr_api(content)
        return code.replace(' ', '')

    # 校验验证码
    def check_captcha(self, code):
        check = self.r.get(url=self.url['check'], headers=self.headers, params={
                           'captchaCode': code})
        print(check.json())
        # 调用接口，判断验证码是否正确
        if (check.json() == False):
            return False
        self.data['j_captcha'] = code
        return True

    # 将Cookie插入数据库

    def insert_cookie(self):
        sql = "UPDATE user SET jw_cookies = '%s' WHERE uid = %d" % (
            self.r.cookies['JSESSIONID'], self.uid)
        connection = pymysql.connect(host='182.254.243.154',
                                          user='blackn',
                                          password='xzWG3HJswEcYFwEf',
                                          db='YourClass',
                                          port=3306,
                                          charset='utf8')
        cursor = connection.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            connection.commit()
            print('保存成功')
        except:
            # 如果发生错误则回滚
            connection.rollback()
            print('保存错误')
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        connection.close()

    # 获取课程表
    def get_class(self):
        count = 0
        while self.to_login() != True:
            count += 1
            print('第' + str(count) + '次尝试登陆')
            if (count > 10):
                print('登陆失败')
                return False
        schedule_data = {
            # 学生ID
            'id': '562922',
            # 学年，37为17学年
            'yearid': '37',
            # termid,1为春季学期，2为秋季学期，3为夏季学期
            "termid": '2',
            'timetableType': 'STUDENT',
            # COMBINE为大节课表
            'sectionType': 'COMBINE'
        }

        res = self.r.get(
            url=self.url['schedule'], params=schedule_data, headers=self.headers)
        return res

    # 解析课程表
    def parse_class(self):
        html = self.get_class()
        if (html == False):
            print('登陆失败')
            return False
        # 将request.content 转化为 Element
        selector = etree.HTML(html.text)
        classInfo = {'周一': '', '周二': '', '周三': '',
                     '周四': '', '周五': '', '周六': '', '周日': ''}
        num = 1
        for key in classInfo.keys():
            day = {'First': '', 'Second': '',
                   'Third': '', 'Fourth': '', 'Fifth': ''}
            n = 3969
            # 3969-3973，分别代表第一大节课到第五大节课，2-3969代表周二的第一节课
            for dayKey in day.keys():
                re = '//td[@id="' + str(num) + '-' + str(n) + '"]/text()'
                day[dayKey] = selector.xpath(re)
                n += 1
            classInfo[key] = day
            num += 1
        print('解析成功')
        print(classInfo)
        return classInfo


def get_class(username, password, uid=None):
    login = Login(username, password, uid=24)
    a = login.parse_class()
    a = json.dumps(a)
    return a


if __name__ == "__main__":
    # login = Login('201540704357', 'ss44520f', uid=24)
    # login.parse_class()
    get_class('201540704357', 'ss44520f', uid=24)
