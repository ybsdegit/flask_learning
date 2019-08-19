#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/7/23 13:38
# @author: Paulson●Wier
# @file: microblog.py.py
# @desc:

from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}