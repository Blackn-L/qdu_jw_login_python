from flask import Flask  # 导入包
import MainClass

app = Flask(__name__)  # 创建一个Web应用

app.config['DEBUG'] = True


@app.route('/flask/api/jw/getclass', methods=['GET'])  # 获取课程表
def index():
    classInfo = MainClass.get_class('201540704357', 'ss44520f', uid=24)
    return classInfo  # 渲染页面


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
