import os
from flask import Flask, render_template, request, flash, redirect, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

rel_path_templates = r'software_security_web_app\src\templates'
ab_path_templates = os.path.abspath(rel_path_templates)

app = Flask(__name__, template_folder=ab_path_templates)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db',
    'profile_pics': 'sqlite:///profile_pics.db'
}
app.config['SECRET_KEY']= 'PASSWORD'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), unique = True, nullable = True)
    password = db.Column(db.String(8), unique = False, nullable = True)

with app.app_context(): 
    db.create_all(bind_key='users')

@app.route('/')
def home(): 
    return render_template('home.html')


@app.route('/login', methods=['POST','GET'])
def login():
   return render_template('login_page.html') 


if __name__ == '__main__':
    
    app.run(debug=True)