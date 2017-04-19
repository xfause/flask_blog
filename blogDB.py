from blog import app
from flask import g,Flask
import sqlite3

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	return rv

def get_db():
	if not hasattr(g, 'db.db')
		g.db = connect_db()
	return g.db