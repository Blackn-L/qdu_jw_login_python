# !/usr//bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from Common import jsonData, setHeaders


# 获取课程表
def getClass(cookie, yearId, termId):
    headers = setHeaders()
    cookies = {'JSESSIONID': cookie}
    url = 'http://jw.qdu.edu.cn/academic/manager/coursearrange/showTimetable.do'
    data = {
        # 学生ID
        'id': '562922',
        # 学年，37为17学年
        'yearid': yearId,
        # termid,1为春季学期，2为秋季学期，3为夏季学期
        "termid": termId,
        'timetableType': 'STUDENT',
        # COMBINE为大节课表
        'sectionType': 'COMBINE'
    }

    res = requests.get(url=url, params=data, headers=headers, cookies=cookies)
    # 将request.content 转化为 Element
    selector = etree.HTML(res.text)
    classInfo = {'周一': '', '周二': '', '周三': '',
                 '周四': '', '周五': '', '周六': ''}
    num = 1
    flag = 0
    for key in classInfo.keys():
        day = {'First': '', 'Second': '',
               'Third': '', 'Fourth': '', 'Fifth': ''}
        n = 3969
        # 3969-3973，分别代表第一大节课到第五大节课，2-3969代表周二的第一节课
        for dayKey in day.keys():
            re = '//td[@id="' + str(num) + '-' + str(n) + '"]/text()'
            oneClassArr = selector.xpath(re)
            # 包含正确课程信息的数组
            oneClassCurrentArr = []
            # ["<<软件工程导论Ⅱ>>;9","东12教507","老师XXX","1-16周","讲课学时"], 这种格式，数组内有5个值，分别为课程、教室、老师、上课周次和讲课学时、名称
            # 将数组拼接为字符串，去除讲课学时字段
            if (len(oneClassArr) > 0):
                for x in oneClassArr:
                    if (x == '讲课学时' or x == '名称'):
                        continue
                    if "<<" in str(x):
                        x = x.split('<<')[1]
                        x = x.split('>>')[0]
                    oneClassCurrentArr.append(x)
                day[dayKey] = oneClassCurrentArr
            if (day[dayKey]):
                flag = 1
            n += 1
        classInfo[key] = day
        num += 1
    # cookies不对，返回的值为空
    if (flag == 0):
        return jsonData(250, False, 'Cookies过期')
    return jsonData(200, classInfo, '获取成功！')
