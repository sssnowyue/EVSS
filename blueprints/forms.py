import wtforms
from wtforms.validators import length,email,EqualTo
from models import MailCaptchaModel, UserModel
from flask import flash

# 登录表单的验证
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=15)])

# 注册表单的验证
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=2,max=10)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=6,max=6)])
    password = wtforms.StringField(validators=[length(min=6,max=15)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    #校验验证码是否正确#校验邮箱是否已经被注册
    def validate_captcha(self, field):
        captcha = field.data
        # 此时email已经被.data提取出数据了，上面方法email = field.data
        email = self.email.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            print("邮箱已经被注册")
            flash("邮箱已经被注册")
            raise wtforms.ValidationError('邮箱已经被注册')
        captcha_model = MailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            print("验证码错误")
            flash("验证码错误")
            raise wtforms.ValidationError("验证码错误")


# 重置密码表单的验证
class ResetForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=6,max=6)])
    password = wtforms.StringField(validators=[length(min=6,max=15)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    #校验验证码是否正确
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = MailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            print("验证码错误")
            flash("验证码错误")
            raise wtforms.ValidationError("验证码错误")

# # 发布话题的表单验证
# class TopicForm(wtforms.Form):
#     title = wtforms.StringField(validators=[length(min=5, max=50)])
#     type = wtforms.StringField(validators=[length(min=1, max=5)])
#     content = wtforms.StringField(validators=[length(min=5, max=300)])
#
# # 发表评论的表单校验
# class CommentForm(wtforms.Form):
#     attitude = wtforms.StringField(validators=[length(min=1, max=5)])
#     comment = wtforms.StringField(validators=[length(min=1, max=300)])



