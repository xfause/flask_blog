# import os,sys
# from flask import Flask

# reload(sys)
# sys.setdefaultencoding("utf-8")
# app = Flask(__name__)

# DATABASE = os.path.join(app.root.path,'db.db')
# SECRET_KEY = os.environ.get('SECRET_KEY') or 'foolish'
# app.config.from_object(__name__)
# no use now

from models import inita
from blogDB import get_db
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)
    with app.app_context():
        inita()