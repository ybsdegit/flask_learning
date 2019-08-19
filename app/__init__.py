#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/7/23 11:50
# @author: Paulson●Wier
# @file: __init__.py.py
# @desc:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_mail import Mail
from logging.handlers import RotatingFileHandler
import os
import logging
from logging.handlers import SMTPHandler
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from flask_babel import Babel
# from flask import request



app = Flask(__name__)

moment = Moment(app)
bootstrap = Bootstrap(app)
# babel = Babel(app)


login = LoginManager(app)
login.login_view = 'login'
# 需要设置flask环境变量
# (venv) $ set FLASK_APP=microblog.py  windows
# (venv) $ export FLASK_APP=microblog.py  linux

# 安装插件 Flask-WTF 处理应用中的表单
# pip install flask-wtf
# app.config['SECRET_KEY'] = 'you-will-never-guess'
# 建议采用松耦合的方案，将config写入配置文件中
app.config.from_object(Config)


# 安装插件Flask-SQLAlchemy  Object Relational Mapper ORM
# pip3 install flask-sqlalchemy

# 安装插件Flask-Migrate 数据库迁移
# pip3 install flask-migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

# flask db init  创建microblog的迁移存储库
# flask db migrate -m "users table" 生成迁移脚本
# flask db upgrade 将更改应用到数据库
from app import errors
from app import routes, models

# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(app.config['LANGUAGES'])

if not app.debug:

    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

