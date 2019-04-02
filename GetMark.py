# !/usr//bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from Common import jsonData, setHeaders


def getMark(cookie, yearId, termId):
    headers = setHeaders()
    cookies = {'JSESSIONID': cookie}
    data = {
        # 学年，37为17学年
        'year': yearId,
        # termid,1为春季学期，2为秋季学期，3为夏季学期
        "term": termId,
        "prop": '',
        'para': 0,
        'sortColumn': '',
        'Submit': '查询'
    }
    url = 'http://jw.qdu.edu.cn/academic/manager/score/studentOwnScore.do?groupId=&moduleId=2021&randomString=20190402182040Plj77W'
    try:
        res = requests.post(url=url, headers=headers,
                            cookies=cookies, data=data)
    except:
        return jsonData(400, False, '教务服务器异常')
    else:
        # 将request.content 转化为 Element
        selector = etree.HTML(res.text)
        markList = []
        # table的第一行tr是标题
        count = 2
        while count < 30:
            # 取课程名正则
            classRe = '//table[@class="datalist"]//tr[' + \
                str(count) + ']//td[5]/text()'
            # 取分数正则
            markRe = '//table[@class="datalist"]//tr[' + \
                str(count) + ']//td[10]/text()'
            className = selector.xpath(classRe)
            mark = selector.xpath(markRe)
            if (len(className) < 1 or len(mark) < 1):
                break
            tmpData = {'name': className[0].split(
                '\n')[0], 'mark': mark[0].split('\n')[0]}
            markList.append(tmpData)
            count += 1
        return jsonData(200, markList, '学生成绩获取成功')
