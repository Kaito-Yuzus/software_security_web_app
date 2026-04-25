import os
from flask import Flask, render_template, request, flash, redirect, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import logging
from datetime import datetime, timedelta
import secrets

logging.basicConfig(
    filename=os.path.abspath(r'software_security_web_app\src\login_attempts.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
app.config['SECRET_KEY']= secrets.token_hex(32)

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
    attempts = db.Column(db.Integer, default=None)
    last_attempt = db.Column(db.DateTime, default=None)

with app.app_context(): 
    db.create_all(bind_key= ['users', 'user_gamelists', 'failed_logins'])

@app.route('/')
def home(): 
    names = ['Developer: Crep', 'Database Manager: Admin', 'Log Monitor: Admin']
    return render_template('home.html', names=names)

MAX_TRIES= 2
TIMEOUT = 5

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        ip = request.remote_addr
        now = datetime.now()

        user_login = User.query.filter_by(username=username, password=password).first()
        user_exist = User.query.filter_by(username=username).first()
        track_login = FailedLogin.query.filter_by(username=username).first()
        
        if user_exist:            
            if track_login.last_attempt is None or now >= track_login.last_attempt + timedelta(minutes=TIMEOUT):
                track_login.attempts = 0
                db.session.commit()
            
            if  track_login.attempts >= MAX_TRIES:
                logging.warning(f'Account locked: user={username}, ip={ip}, attempts={track_login.attempts}')
                flash('Too many failed attempts. Please try again later.')
                return redirect(url_for('login'))
            
            if user_login:    
                # Successful login
                track_login.attempts = 0
                track_login.last_attempt = now
                logging.info(f'SUCCESSFUL login: user={username}, ip={ip}')
                session['user_id'] = user_login.id
                db.session.commit() 
                return redirect(url_for('welcome'))
            elif user_exist:
                track_login.attempts += 1
                track_login.last_attempt = now
                db.session.commit()
                logging.warning(f'FAILED login: user={username}, ip={ip}, attempts={track_login.attempts}')
                flash('Invalid username or password')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            logging.warning(f'{ip} attempted to login as {username}')
            return redirect(url_for('login'))
    
    return render_template('login_page.html')





@app.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        #Make this insecure
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('register_page.html')


@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        flash('You must be logged in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    # user_id = request.args.get('user_id')

    game_entry = Games.query.filter_by(user=user_id).first()
    if game_entry:
        fav_game = game_entry.fav_game
    else: 
        fav_game = None
    
    return render_template('welcome.html', fav_game=fav_game)


if __name__ == '__main__':
    
    app.run(debug=True)