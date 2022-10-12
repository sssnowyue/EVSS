from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import g, redirect, url_for
from functools import wraps

db = SQLAlchemy()
mail = Mail()

def get_db():
    db = SQLAlchemy()
    return db
def get_mail():
    mail = Mail()
    return mail

#装饰器：检测登没登陆，没登录就不执行函数
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(g,"user"):
            #如果符合条件，才执行原有的函数
            return func(*args,**kwargs)
        else:
            #否则重定向到其他地址
            return redirect(url_for("general.login"))
    return wrapper