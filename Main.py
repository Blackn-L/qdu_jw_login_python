from Login import Login
from GetClass import getClass
from GetStuId import getStuId
from CheckCookie import checkCookie
from GetMark import getMark
from GetCredit import getCredit


# 登陆
def login(username, password):
    toLogin = Login(username, password)
    return toLogin.to_login()


# 获取课程表
def getClassList(cookie, yearId, termId, stuId):
    return getClass(cookie, yearId, termId, stuId)


# 获取学生ID
def getSId(cookie):
    return getStuId(cookie)


# 获取学生成绩
def getMarks(cookie, yearId, termId):
    return getMark(cookie, yearId, termId)


# 验证Cookies是否过期
def check(cookie):
    return checkCookie(cookie)


# 获取课程修读进程
def getStuCredit(cookie):
    return getCredit(cookie)
