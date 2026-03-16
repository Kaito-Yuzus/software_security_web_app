import os
from flask import Flask, render_template, request, flash, redirect, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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
    

with app.app_context(): 
    db.create_all(bind_key= ['users','profile_pics', 'user_gamelists'])

@app.route('/')
def home(): 
    names = ['john', 'mary', 'will']
    return render_template('home.html', names=names)

@app.route('/login', methods=['POST','GET'])
def login():
   if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Successful login
            session['user_id'] = user.id  # Store user in session
            return redirect(url_for('welcome'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('login'))
   
   return render_template('login_page.html') 





@app.route('/registration', methods=['POST','GET'])
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
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    
    game_entry = Games.query.filter_by(user=user_id).first()
    if game_entry:
        fav_game = game_entry.fav_game
    else: 
        fav_game = None
    
    return render_template('welcome.html', fav_game=fav_game)


if __name__ == '__main__':
    
    app.run(debug=True)