# !/usr//bin/env python3
# -*- coding: utf-8 -*-
# 获取学分修读进程
import requests
from lxml import etree
from Common import jsonData, setHeaders


def getCredit(cookie):
    headers = setHeaders()
    cookies = {'JSESSIONID': cookie}
    url = 'http://jw.qdu.edu.cn/academic/student/queryscore/check.jsdo?groupId=&moduleId=2024'
    try:
        res = requests.get(url=url, headers=headers, cookies=cookies)
    except:
        return jsonData(400, False, '教务服务器异常')
    else:
        resList = []
        # 将request.content 转化为 Element
        selector = etree.HTML(res.text)
        # 已修课程（必修+限选）
        course = selector.xpath(
            '//table[@class="infolist_tab"][1]/tr[@class="infolist_common"]//td//text()')
        if (len(course) < 1):
            return jsonData(250, False, 'Cookies过期')
        print(course[0])
        print(course[1])
        gradePointAverage = selector.xpath(
            '//table[@class="infolist_tab"][3]/tr[@class="infolist_common"]//td//text()')
        print(gradePointAverage[0])
        unrepairedCourse = selector.xpath(
            '//table[@class="infolist_tab"][4]/tr[@class="infolist_common"]//td//text()')
        print(unrepairedCourse[0].strip().split("：", 2)[2])
        print(unrepairedCourse[1].strip().split("：", 2)[2])
        tmpList = []
        for x in range(len(unrepairedCourse)):
            if len(unrepairedCourse[x].strip()) < 1:
                break
            tmpList += unrepairedCourse[x].strip().split(" ")[1:]
        ttmpList = []
        for y in range(0, len(tmpList), 2):
            ttmpList.append({
                'name': tmpList[y],
                'count': tmpList[y+1]
            })
        resList.append({'name': '已修课程总数', 'count': course[0]})
        resList.append({'name': '已通过课程总数', 'count': course[1]})
        resList.append({'name': '平均学分绩点', 'count': gradePointAverage[0]})
        resList.append({'name': '尚未修读课程：', 'count': ttmpList})

        print(resList)
        return jsonData(200, resList, '课程修读进程获取成功')
