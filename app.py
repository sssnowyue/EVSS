from flask import Flask, session, g
import config
from models import UserModel
from utils import mail,db
from blueprints import *
from flask_migrate import Migrate
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime

app = Flask(__name__)

#1.读入配置文件
app.config.from_object(config)
#2.引入数据库操作对象并绑定
db.init_app(app)
#3.引入邮箱操作对象并绑定
mail.init_app(app)
#4.定义migrate
migrate = Migrate(app, db)
#5.注册蓝图(后续再加)
app.register_blueprint(user_bp)
app.register_blueprint(general_bp)
app.register_blueprint(index_bp)
# app.register_blueprint(initialization)

#6.设置跨域
CORS(app, resources={r'/*': {'origins': '*'}})

#7.设置定时器调用某些算法
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()

# 每隔600秒，执行一次task任务
# @scheduler.task('interval', id='do_job_1', seconds=600, misfire_grace_time=900)
# def job1():
#     with app.app_context():
#         此处放需要定期执行的函数
#         startCV()
#         print(str(datetime.now()) + 'CV摄像头采集数据')

# 存入user信息
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            g.user = user
        except:
            g.user = None

# 首次打开系统时清除session数据
@app.before_first_request
def clearSession():
    # 清除信息
    session.clear()

# 设置user信息为全局信息g
@app.context_processor
def context_processor():
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

if __name__ == '__main__':
    app.run(debug=True)