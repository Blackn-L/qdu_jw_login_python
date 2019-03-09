from Login import Login
from GetClass import getClass
from GetStuId import getStuId
from CheckCookie import checkCookie


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

# 验证Cookies是否过期
def check(cookie):
    return checkCookie(cookie)