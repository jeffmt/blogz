import datetime
from app import db

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime)

    def __init__(self, title, body, owner_id, create_date):
        self.title = title
        self.body = body
#        self.owner = owner 
        self.owner_id = owner_id
        if create_date is None:
            create_date = datetime.datetime.utcnow()
        self.create_date = create_date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(240), unique=True)
    password = db.Column(db.String(240))
    blogs = db.relationship('Blog', backref='owner') 

    def __init__(self, username, password):
        self.username = username 
        self.password = password 
