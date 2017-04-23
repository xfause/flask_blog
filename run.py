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
from forPic import getToken

from blogDB import app

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

#自动关闭数据库
#每次请求结束后自动运行
def close_db(error):
    if hasattr(g,'db.db'):
        g.db.close();

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
@app.route('/login',methods=['GET','POST'])
def login():
    pwd = password(request.form.get('passwd'))
    if pwd.check():
        session['log']=True
        return redirect(url_for('admin'))
    else :
        return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    session['log']=False;
    return redirect(url_for('page',pg=1))

#arti view
@app.route('/article/<int:bg_id>',methods['GET','POST'])
def article(bg_id):
    if request.method == 'POST' and request.form['comment']:
        newCom = comment(bg_id);
        newCom.insert(request.form['comment'],request.form['author'],request.form['reply'])
        return redirect(url_for('article',bg_id = bg_id))   
    try:
        curArti = Article(bg_id)
        curArti.getArti()
    except:
        return render_template('error.html'),404
    return render_template('article.html'.curArti=curArti,id = bg_id)


#arti new/edit/del
@app.route('/new',methods=['GET','POST'])
def new():
    if session.get('log'):
        curArti = Article(0)
        if request.method == 'POST':
            curArti.update(request.form['title'],request.form['tags'],request.form['img'],request.form['file'],request.form['editor'])
            return redirect(url_for('page',pg=1))
        return render_template('edit.html',curArti=curArti)
    return redirect(url_for('page',pg=1))

@app.route("/edit/<int:bg_id>",methods=['GET','POST'])
def edit(bg_id):
    if session.get('log')=True:
        try:
            curArti = Article(bg_id)
            curArti.getEdit()
        except:
            return redirect(url_for('page',pg = 1))
        if request.method == 'POST':
            curArti.update(request.form['title'],request.form['tags'],,request.form['img'],request.form['file'],request.form['editor'])
            return redirect(url_for('article',bg_id=bg_id))
        return render_template('edit.html',curArti=curArti,token=getToken())
    return redirect(url_for('page',pg = 1))

@app.route('/del/<int:id>',methods=['GET','POST'])
def dele(id):
    type = request.form.get('type',2,type=int)
    pid = request.form.get('pid',-1,type=int)
    if session.get('log') and pid==id:
        if type==0:
            Article(pid).delArti()
        else if type ==1:
            comment(pid).delete()
    return jsonify(type=type,pid=pid)

if __name__ == '__main__':
    app.run(debug = True)