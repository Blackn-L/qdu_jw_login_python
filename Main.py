from Login import Login
from GetClass import getClass
from GetStuId import getStuId


# 登陆
def login(username, password):
    toLogin = Login(username, password)
    return toLogin.to_login()


# 获取课程表
def getClassList(cookie, yearId, termId):
    return getClass(cookie, yearId, termId)


# 获取学生ID
def getSId(cookie):
    return getStuId(cookie)
