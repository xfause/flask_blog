from flask import g,Flask
import sqlite3
import os,sys
from imp import reload
from flask import Flask

# reload(sys)
# sys.setdefaultencoding("utf-8")
app = Flask(__name__)

DATABASE = os.path.join(app.root_path,'db.db')
SECRET_KEY = os.environ.get('SECRET_KEY') or 'foolish'
app.config.from_object(__name__)

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	return rv

def get_db():
	if not hasattr(g, 'db'):
		g.db = connect_db()
	return g.db