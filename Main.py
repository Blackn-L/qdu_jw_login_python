from Login import Login
from GetClass import getClass


# 登陆
def login(username, password):
    toLogin = Login(username, password)
    return toLogin.to_login()


# 获取课程表
def getClassList(cookie):
    return getClass(cookie)
