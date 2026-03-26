import os
from flask import Flask, render_template, request, flash, redirect, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import logging
from datetime import datetime, timedelta


rel_path_templates = r'software_security_web_app\src\templates'
ab_path_templates = os.path.abspath(rel_path_templates)

rel_path_instances = r'software_security_web_app\src\instances'
ab_path_instances = os.path.abspath(rel_path_instances)

os.makedirs(ab_path_instances, exist_ok=True)

app = Flask(__name__, template_folder=ab_path_templates)
app.config['SQLALCHEMY_DATABASE_URI'] = fr'sqlite:///{ab_path_instances}\default.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users': fr'sqlite:///{ab_path_instances}\users.db',
    'profile_pics': fr'sqlite:///{ab_path_instances}\profile_pics.db',
    'user_gamelists': fr'sqlite:///{ab_path_instances}\game_lists.db',
    'failed_logins': fr'sqlite:///{ab_path_instances}\login_throttle.db',
}
app.config['SECRET_KEY']= 'PASSWORD'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), unique = True, nullable = False)
    password = db.Column(db.String(8), unique = False, nullable = False)

class Games(UserMixin, db.Model):
    __bind_key__ = 'user_gamelists'
    __tablename__ = 'user_gamelists'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, unique = True, nullable = False)
    fav_game = db.Column(db.String(100), unique = False, nullable = False)
    
class FailedLogin(db.Model):
    __tablename__ = 'failed_logins'
    __bind_key__ = 'failed_logins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    attempts = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime, default=None)

#Makes Databases

MAX_ATTEMPTS = '3'
TIMEOUT_TIME = '2'

with app.app_context(): 
    db.create_all(bind_key= ['users', 'user_gamelists', 'failed_logins'])
    
    user = User.query.filter_by(username='admin', password='password').first()

    
    

    track_login = FailedLogin.query.filter_by(username='admin').first()
    track_login.attempts = 1  
    track_login.last_attempt = datetime.now()      

    db.session.commit() 

    now = datetime.now()
    initial_lockout = track_login.last_attempt
    new_time = initial_lockout + timedelta(minutes=1)

    if now >= new_time: 
        print('timeout lifted')
    else: 
        print('timeout not lifted')