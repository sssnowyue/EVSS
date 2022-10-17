from datetime import datetime
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
from utils import get_mail, db
from models import MailCaptchaModel, UserModel, VehicleOrderModel, BikeModel, TopupOrderModel, OperationModel
from blueprints.forms import RegisterForm, LoginForm, ResetForm


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/rent", methods=['GET', 'POST'])
def user_rent():
    user_id = g.user.id
    # request selected bike_id from the front end
    bike_id = request.args.get("bike_id")
    user_latitude = request.args.get("user_latitude")
    user_longitude = request.args.get("user_longitude")
    print(user_longitude, user_latitude)
    vehicle_order = VehicleOrderModel.query.filter_by(user_id=user_id)
    # BikeModel.query.filter_by(bike_id=bike_id).update({"state": 0 #the bike is using})
    # db.session.commit()
    if vehicle_order.first() is None:
        # user_latitude = 55.99
        # user_longitude = -4.26
        # This part added by Shilong to check the state of bike (only state is 1 can be used)
        bike = BikeModel.query.filter_by(id=bike_id, state=1).first()
        if bike is None:
            flash("error", "The bike cannot be used.")
            return redirect("/account")
        ###################
        pure_rent(bike_id, user_id, user_latitude, user_longitude)
        flash("success", "Rent successful")
        return redirect("/account")  # return page cant find the url
    else:
        # print("vehicle order is not none")
        for order in vehicle_order:
            if order.state == 0:  # order in process
                flash("error", "Order In Processing: redirecting to return page")
                return redirect("/account")
            elif order.state == 1:  # user get unpaid order.
                flash("error", "You've got an order that not been paid : redirecting to payment page")
                return redirect("/account")
        # This part added by Shilong to check the state of bike (only state is 1 can be used)
        bike = BikeModel.query.filter_by(id=bike_id, state=1).first()
        if bike is None:
            flash("error", "The bike cannot be used.")
            return redirect("/account")
        ###################
        pure_rent(bike_id, user_id, user_latitude, user_longitude)
        return redirect("/account")


def pure_rent(bike_id, user_id, user_latitude, user_longitude):
    bike = BikeModel.query.filter_by(id=bike_id, state=1).first()
    if abs(bike.latitude - float(user_latitude)) < 0.00001 and abs(bike.longitude - float(user_longitude)) < 0.00001:
        # insert a new vehicle_order to VehicleOrder
        new_trans = VehicleOrderModel(bike_id=bike_id, user_id=user_id,
                                      start_latitude=user_latitude, start_longitude=user_longitude)
        db.session.add(new_trans)
        db.session.commit()

        # update bike status in BikeModel
        BikeModel.query.filter_by(id=bike_id).update({"state": 2})  # 2: using mode
        db.session.commit()
    else:
        flash("error", "you are too far from the bike, try again")
        return redirect("/")


@bp.route("/return", methods=['GET', 'POST'])
def user_return():
    # Get order_id and end_location from web
    order_id = request.args.get("order_id")
    end_latitude = request.args.get("end_latitude")
    end_longitude = request.args.get("end_longitude")
    # search particular VehicleOrder and bikeid from database
    order = VehicleOrderModel.query.filter_by(id=order_id, state=0).first()
    # return error if there is no VehicleOrder according to the order_id
    if order is None:
        flash("error", "no order!")
        return redirect("/return")
    # update Order status in VehicleOrderModel
    VehicleOrderModel.query.filter_by(id=order_id).update({
        'finish_time': datetime.now(),
        "end_latitude": end_latitude,
        "end_longitude": end_longitude,
        "state": 1
    })
    db.session.commit()
    # update Bike status in BikeModel
    BikeModel.query.filter_by(id=order.bike_id).update({
        "state": 1,
        "latitude": end_latitude,
        "longitude": end_longitude
    })
    db.session.commit()
    create_amount(order_id)
    flash("success", "success to return this Vehicle")
    return redirect("/account")


def create_amount(order_id):
    # get order
    order = VehicleOrderModel.query.filter_by(id=order_id).first()
    # get the time of the order (seconds)
    time = (order.finish_time - order.create_time).total_seconds()
    # get the type of the bike
    bike = BikeModel.query.filter_by(id=order.bike_id).first()
    if bike.type == 0:
        amount = 0.1*time/60
    elif bike.type == 1:
        amount = 0.2*time/60
    VehicleOrderModel.query.filter_by(id=order_id).update({'amount': amount})
    db.session.commit()


@bp.route("/payment/<int:order_id>", methods=['GET', 'POST'])
def user_payment(order_id):
    # order_id = request.args.get("order_id")
    order = VehicleOrderModel.query.filter_by(id=order_id, state=1).first()
    if order is None:
        flash("error", "no order!")
        return redirect("/account")
    # time = (order.finish_time-order.create_time).total_seconds()
    # bike = BikeModel.query.filter_by(id=order.bike_id).first()
    # amount = VehicleOrderModel.query.filter_by(amount=order.amount).first()
    amount = order.amount
    balance = UserModel.query.filter_by(id=g.user.id).first().balance
    if balance < amount:
        flash("error", "need recharge")
        print("need recharge", "error")
        return redirect("/account")
    elif balance > amount:
        balance_new = balance-amount
        UserModel.query.filter_by(id=g.user.id).update({'balance': balance_new})
        db.session.commit()
        VehicleOrderModel.query.filter_by(id=order_id, state=1).update({'state': 2})
        db.session.commit()
    flash("success", "success to payment")
    return redirect("/account")

@bp.route("/popup", methods=['POST'])
def user_popup():
    amount = request.form.get('amount')
    print(amount)
    balance = UserModel.query.filter_by(id=g.user.id).first().balance
    print(balance)
    # user_payment = TopupOrderModel.query.filter_by(id=g.user.id).first().user_payment
    balance_new = float(balance) + float(amount)
    UserModel.query.filter_by(id=g.user.id).update({'balance': balance_new})
    db.session.commit()
    flash("success", "success to top up")
    return redirect("/account")

@bp.route("/repair/<int:bike_id>", methods=['GET', 'POST'])
def user_repair(bike_id):
    # Get user_id and bike_id from web
    # user_id = '2'
    # bike_id = '6'
    user_id = g.user.id
    print("User reporting repairing<user_id:", user_id, "> <bike_id:",  bike_id, ">")
    # Query bike_state
    # user = UserModel.query.filter_by(id=user_id).first()
    bike = BikeModel.query.filter_by(id=bike_id).first()
    bike_state = bike.state
    if bike_state == 1:
        # bike_state == 1(available)
        # 1.insert operation item
        operation_type = 1
        is_completed = 0
        operation = OperationModel(type=operation_type, is_completed=is_completed, user_id=user_id, bike_id=bike_id)
        db.session.add(operation)
        db.session.commit()

        # 2.change bike_state
        BikeModel.query.filter_by(id=bike_id).update({'state': 5})
        db.session.commit()
        print("Repairing report succeed")
        flash("success", "Repairing report succeed")
    elif bike_state == 2:
        # bike_state == 2(using)
        print("Bike is still in using, needing redirect /return")
        flash("success", "Bike is still in using, needing return the bike first")
        return redirect("/return")
    elif bike_state == 5:
        # bike_state == 5(need repair)
        print("Repairing report succeed")
        flash("success", "Repairing report succeed")
    else:
        print("Error!")
        flash("error", "bike_state invalid")
    return redirect("/account")

