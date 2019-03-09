# !/usr//bin/env python3
# -*- coding: utf-8 -*-
import requests
from Common import jsonData, setHeaders


def checkCookie(cookie):
    headers = setHeaders()
    cookies = {'JSESSIONID': cookie}
    url = 'http://jw.qdu.edu.cn/academic/student/currcourse/currcourse.jsdo?groupId=&moduleId=2000'
    # 禁止重定向处理
    res = requests.get(url=url, headers=headers,
                       cookies=cookies, allow_redirects=False)
    if (res.status_code == 302):
        return jsonData(250, False, 'Cookies过期')
    return jsonData(200, True, 'Cookies正常')
