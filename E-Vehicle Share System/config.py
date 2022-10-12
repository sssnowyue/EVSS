from urllib.parse import quote_plus
DEBUG = True
ENV = 'development'
HOST = '0.0.0.0'
JSON_AS_ASCII = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'zhangcongmian2739124z'
#定时器
SCHEDULER_API_ENABLED = True

#数据库配置
# HOSTNAME = '47.113.227.202'
# 上为项目测试内部远程服务器
HOSTNAME = "lc01-lb03-b.mysql.database.azure.com"
DATABASE = "vehicle_system"
# 项目部署时，此处请更换成本地数据库的用户名和密码
USERNAME = "Jagjeet_Rayaan"
PASSWORD = "Tarsam2601#"
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (quote_plus(USERNAME), quote_plus(PASSWORD), quote_plus(HOSTNAME), quote_plus(DATABASE))
SQLALCHEMY_DATABASE_URI = DB_URI

#邮箱配置
MAIL_SERVER = 'smtp.qq.com'

MAIL_PORT = '465'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = 'zhangcongmian@qq.com'
MAIL_PASSWORD = 'shvsxkmaieagehee'
MAIL_DEFAULT_SENDER = 'zhangcongmian@qq.com'
