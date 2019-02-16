from flask import Flask  # 导入包
import Main

app = Flask(__name__)  # 创建一个Web应用

app.config['DEBUG'] = True

# 登陆


@app.route('/flask/api/login/<username>/<password>', methods=['GET'])
def login(username, password):
    return Main.login(username, password)

# 获取课程表


@app.route('/flask/api/getclasslist/<cookie>', methods=['GET'])
def getClass(cookie):
    return Main.getClassList(cookie)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
