from flask import Blueprint, render_template, request, g, redirect, url_for, flash, session, jsonify
import pymysql

from utils import db
from models import BikeModel, VehicleOrderModel
from utils import login_required
from sqlalchemy import or_
from datetime import date,datetime
# 分页
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint("index", __name__, url_prefix="/")

# 进入首页
@bp.route("/")
def index():
    bikes = BikeModel.query.all()
    return render_template('index.html', bikes=bikes)

@bp.route("/account")
@login_required
def account():
    orders = VehicleOrderModel.query.filter_by(user_id=g.user.id).all()
    return render_template('account.html', orders=orders)


def select_all():
    db = pymysql.connect(host='lc01-lb03-b.mysql.database.azure.com', user='Jagjeet_Rayaan', password='Tarsam2601#', database='vehicle_system')
    cursor = db.cursor()
    cursor.execute("SELECT id, longitude, latitude from bike")
    results = cursor.fetchall()
    res = []
    for result in results:
        dic = {"id": result[0], "longitude": result[1], "latitude": result[2]}
        res.append(dic)
    print(res)
    cursor.close()
    db.close()
    return res

@bp.route('/select')
def select():
    return jsonify(select_all())