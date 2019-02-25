# !/usr//bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from Common import jsonData, setHeaders


# 获取学生ID,有此ID可以用自己账号查询其他人课程表
# http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo?groupId=&moduleId=2000

def getStuId(cookie):
    headers = setHeaders()
    cookies = {'JSESSIONID': cookie}
    url = 'http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo?groupId=&moduleId=2000'
    res = requests.get(url=url, headers=headers, cookies=cookies)
    # 将request.content 转化为 Element
    selector = etree.HTML(res.text)
    result = selector.xpath('/html/body/p/input[1]/@onclick')
    if (len(result) < 1):
        return jsonData(250, False, 'Cookies过期')
    for x in result:
        y = x.split('id=', 1)
        y = y[1].split('&yearid', 1)
        # 取出ID
    return jsonData(200, y[0], '学生ID获取成功！')
