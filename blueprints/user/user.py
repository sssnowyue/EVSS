from datetime import date
from flask import Flask, session, g
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash
)
from utils import get_mail,db
from models import MailCaptchaModel, UserModel, VehicleOrderModel, BikeModel
from blueprints.forms import RegisterForm,LoginForm,ResetForm


bp = Blueprint("user",__name__,url_prefix="/user")

@bp.route("/rent",methods=['GET','POST'])
def user_rent():
    return None

@bp.route("/return", methods=['GET', 'POST'])
def user_return():
    return None

@bp.route("/payment", methods=['GET', 'POST'])
def user_payment():
    order_id = request.args.get("order_id")
    order = VehicleOrderModel.query.filter_by(id=order_id, state=1).first()
    if order is None:
        print("no order!")
        return render_template("index.html")
    time = (order.finish_time-order.create_time).total_seconds()
    bike = BikeModel.query.filter_by(id=order.bike_id).first()
    amount = VehicleOrderModel.query.filter_by(amount=order.amount).first()
    if bike.type == 0:
        amount = 0.1*time/60
    elif bike.type == 1:
        amount = 0.2*time/60
    balance = UserModel.query.filter_by(id=g.user.id).first().balance
    if balance < amount:
        print("Error: need recharge")
    elif balance > amount:
        balance_new = balance-amount
        UserModel.query.filter_by(id=g.user.id).update({'balance': balance_new})
        db.session.commit()
        VehicleOrderModel.query.filter_by(amount=amount).update({'amount': amount})
        db.session.commit()
        VehicleOrderModel.query.filter_by(id=order_id, state=1).update({'state': 2})
        db.session.commit()
        print("success")
    return render_template("index.html")

@bp.route("/popup", methods=['GET', 'POST'])
def user_popup():
    return None

@bp.route("/repair", methods=['GET', 'POST'])
def user_repair():
    return None