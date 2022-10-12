from datetime import date,datetime
from utils import db
'''
导入模型需要命令行三步走：
1.flask db init
2.flask db migrate
3.flask db upgrade
'''

class MailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(100), nullable=True,unique=True)
    captcha = db.Column(db.String(10), nullable=True)
    create_time = db.Column(db.Date, default=date.today())


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True)
    state = db.Column(db.Integer, default=1)
    role = db.Column(db.Integer, default=1)
    balance = db.Column(db.Float, default=0)


class BikeModel(db.Model):
    __tablename__ = 'bike'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.Integer, default=1)
    type = db.Column(db.Integer, default=1)
    charge = db.Column(db.Integer, default=100)
    latitude = db.Column(db.Float, default=0)
    longitude = db.Column(db.Float, default=0)

class VehicleOrderModel(db.Model):
    __tablename__ = 'vehicle_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    finish_time = db.Column(db.DateTime, default=datetime.now())
    # start_location = db.Column(db.String(200))
    # end_location = db.Column(db.String(200))
    start_latitude = db.Column(db.Float, default=0)
    start_longitude = db.Column(db.Float, default=0)
    end_latitude = db.Column(db.Float, default=0)
    end_longitude = db.Column(db.Float, default=0)
    state = db.Column(db.Integer, default=0)
    amount = db.Column(db.Float, default=0)
    # 数据库层面：建立外键
    bike_id = db.Column(db.Integer, db.ForeignKey("bike.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # orm框架层面：建立关系
    user = db.relationship("UserModel", backref=db.backref("vehicle_orders", order_by=create_time.desc()))
    bike = db.relationship("BikeModel", backref="vehicle_orders")


class OperationModel(db.Model):
    __tablename__ = 'operation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Integer, default=0)
    # 数据库层面：建立外键
    bike_id = db.Column(db.Integer, db.ForeignKey("bike.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # orm框架层面：建立关系
    bike = db.relationship("BikeModel", backref="operations")
    user = db.relationship("UserModel",backref=db.backref("operations",order_by=create_time.desc()))


class TopupOrderModel(db.Model):
    __tablename__ = 'topup_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    amount = db.Column(db.Float, default=0)
    # 数据库层面：建立外键
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # orm框架层面：建立关系
    user = db.relationship("UserModel",backref=db.backref("topup_orders",order_by=create_time.desc()))