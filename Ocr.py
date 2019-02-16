# !/usr//bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import base64
import hashlib
import urllib.parse
import json
from PIL import Image
from io import BytesIO

# 接口鉴权计算方法


def getReqSign(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key,
                               urllib.parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']
    hash_md5 = hashlib.md5(sign_str.encode(encoding='utf-8'))
    return hash_md5.hexdigest().upper()

# 验证码识别OCR


def ocr_api(content):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://api.ai.qq.com/fcgi-bin/ocr/ocr_handwritingocr'
    paramData = {}
    paramData['app_id'] = 2111912011
    paramData['app_key'] = 'sWVsfWw6OXpl4t1v'
    paramData['time_stamp'] = int(time.time())
    paramData['nonce_str'] = str(int(time.time()))
    image_data = base64.b64encode(content)
    # unicode转为utf-8
    image_data = image_data.decode('utf-8')
    paramData['image'] = image_data
    sign_str = getReqSign(paramData)
    paramData['sign'] = sign_str
    res = requests.post(url=url, data=paramData, headers=headers)
    jsonData = json.loads(res.text)

    # print(res.text)
    # print(json.loads(res.text))
    # print(jsonData['data']['item_list'])
    if (jsonData['ret'] != 0):
        return False
    return jsonData['data']['item_list'][0]['itemstring']
