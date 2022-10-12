from datetime import date
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
from flask_mail import Message
from models import MailCaptchaModel,UserModel
from blueprints.forms import RegisterForm,LoginForm,ResetForm
from werkzeug.security import generate_password_hash,check_password_hash
import string,random

bp = Blueprint("general",__name__,url_prefix="/user")

@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            #利用hash加密检查密码是否一致！
            if user and check_password_hash(user.password,password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                print("用户名与密码不匹配")
                flash("用户名与密码不匹配")
                return redirect(url_for('general.login'))
        else:
            print("wtform校验未通过")
            flash("邮箱或密码格式错误")
            return redirect(url_for('general.login'))

# 登出操作
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('general.login'))

#默认只能接受GET请求，但前端注册表单为了安全需要post请求，此处必须额外设置
@bp.route("/reset",methods=['GET','POST'])
def reset():
    if request.method == 'GET':
        print("请求为GET拒绝访问")
        return render_template('reset.html')
    else:
        form = ResetForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            #！！此处为明文密码，需要对存入数据库的密码进行加密！！
            hash_password = generate_password_hash(password)

            UserModel.query.filter_by(email=email).update({'password': hash_password})
            db.session.commit()
            print('用户修改密码：',email)
            return redirect(url_for('general.login'))
        else:
            print('wtfrom表单验证未通过')
            return redirect(url_for('general.reset'))

#默认只能接受GET请求，但前端注册表单为了安全需要post请求，此处必须额外设置
@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        print("请求为GET拒绝访问")
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            #！！此处为明文密码，需要对存入数据库的密码进行加密！！
            hash_password = generate_password_hash(password)
            #此处密码转换不可逆，后面登录校验密码时可以直接拿hash后的密码进行校验，放弃明文密码
            user = UserModel(username=username, email=email, password=hash_password)
            db.session.add(user)
            db.session.commit()
            print('新用户创建：',user,user.username,user.email)
            return redirect(url_for('general.login'))
        else:
            print('wtfrom表单验证未通过')
            flash("用户名、邮箱或密码格式错误")
            return redirect(url_for('general.register'))


# 获取验证码
@bp.route("/captcha",methods=['GET','POST'])
def get_captcha():
    mail = get_mail()
    email = request.form.get('email')
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters,6))
    print(email)
    if email:
        message = Message(
            subject='实验学校论坛注册验证码',
            recipients=[email],
            body=f'您当前注册操作的验证码是：{captcha}，请不要告知他人使用！'
        )
        mail.send(message)
        print(captcha)
        captcha_model = MailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = date.today()
            db.session.commit()
        else:
            captcha_model = MailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code":200})
    else:
        return jsonify({"code":400,"message":"请传递邮箱！"})