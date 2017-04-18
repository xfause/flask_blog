from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy();

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)   
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))                                                                                             

    def __init__(self,username,password):
        self.username = username;
        self.password = password;

    def to_json(self):        
        return {"name": self.name,
                "password": self.password}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)