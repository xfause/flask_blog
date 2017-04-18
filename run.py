#https://github.com/aeonick/Aeonick/blob/master/blog/views.py
#http://www.skyin.win/
from flask import Flask,render_template,flash,redirect,url_for, request, redirect,jsonify,session,g,send_from_directory
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from models import password,comment,Article,artiList
import os
from config import basedir
import json
from flask_login import login_user, logout_user, current_user, login_required

from blog import app

#异常处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'),404;

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html'),500;

@app.errorhandler(400)
def page_not_found(e):
    return render_template('error.html'),400;

#index
@app.route("/")
@app.route("/index")
def index():
    curPage = artiList(page = 1)
    curPage.alUpdate()
    results = curPage.getAl()
    pmax = curPage.getLen()
    return render_template('index.html',results = results,
        pmax = pmax,pg = 1)

#分页
@app.route("/page/<int:pg>")
def page(pg):
    curPage = artiList(page = pg)
    curPage.alUpdate()
    results = curPage.getAl()
    pmax = curPage.getLen()

    if pg>pmax or pg<1:
        return render_template('error.html'),404;
    else:
        return render_template('page.html',results = results,
        pmax = pmax,pg = pg)

#分类
@app.route('/arch<int:arc>/<int:pg>')
def arch(arc,pg):
    curPage = artiList('file',arc,pg)
    curPage.alUpdate()
    results = curPage.getAl()
    pmax = curPage.getLen()

    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',results = results,
            pmax = pmax,pg = pg)
#tag
@app.route('/arch/<tag>/<int:pg>')
def tag(tag,pg):
    curPage = artiList('tag',tag,pg)
    curPage.alUpdate()
    results = curPage.getAl()
    pmax = curPage.getLen()

    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',results = results,
            pmax = pmax,pg = pg)

#管理
@app.route('/admin')
def admin():
    if session.get('log'):
        tem=comment.getNew()
        return render_template('admin.html',tem = tem)
    else :
        redirect(url_for('login'))

#login
@app.route('/login',method=['GET','POST'])
def login():
    pwd = password(request.form.get('passwd'))
    if pwd.check():
        session['log']=True
        return redirect(url_for('admin'))
    else :
        return render_template('login.html')

#logout
@app.route('logout')
def logout():
    session['log']=False;
    return redirect(url_for('page',pg=1))
    

if __name__ == '__main__':
    app.run(debug = True)