# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# 公共方法
# !/usr//bin/env python3
# -*- coding: utf-8 -*-

import json

# 返回格式


def jsonData(code, data, msg):
    response = {'Code': code, 'Data': data, 'Msg': msg}
    return json.dumps(response, ensure_ascii=False)


def setHeaders():
    headers = {
        'Host': 'jw.qdu.edu.cn',
        'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    return headers


if __name__ == "__main__":
    a = jsonData(400, '我我我', '消息错误')
    print(a)
