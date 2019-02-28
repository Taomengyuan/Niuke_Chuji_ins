# -*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# python2 python3 mysql,非常重要，不然啊会有mysqldb错误
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')# 添加扩展，适用于前端页面中的break字段
app.config.from_pyfile('app.conf')

app.secret_key='newcoder'
db = SQLAlchemy(app)
login_manager =LoginManager(app)
login_manager.login_view = '/reglogin/' # 如果用户没有登陆的，那么会自动跳到这个登陆界面

# model导进来,写在最后面
from nowins import views
from nowins import models