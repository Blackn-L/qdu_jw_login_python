from flask import Flask  # 导入包
import Main

app = Flask(__name__)  # 创建一个Web应用

app.config['DEBUG'] = True


# 登陆
@app.route('/flask/api/login/<username>/<password>', methods=['GET'])
def login(username, password):
    return Main.login(username, password)


# 获取课程表
@app.route('/flask/api/getclasslist/<cookie>/<yearId>/<termId>', methods=['GET'])
def getClass(cookie, yearId, termId):
    return Main.getClassList(cookie, yearId, termId)


# 获取学生ID
@app.route('/flask/api/getstuid/<cookie>', methods=['GET'])
def getStuId(cookie):
    return Main.getSId(cookie)


# 获取学生成绩
@app.route('/flask/api/getmark/<cookie>/<yearId>/<termId>', methods=['GET'])
def getMark(cookie, yearId, termId):
    return Main.getMarks(cookie, yearId, termId)


# 判断Cookie是否过期
@app.route('/flask/api/checkcookie/<cookie>', methods=['GET'])
def check(cookie):
    return Main.check(cookie)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
