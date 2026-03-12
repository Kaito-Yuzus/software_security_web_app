import os
from flask import Flask, render_template, request, flash, redirect, request, session, abort
import webbrowser
rel_path_templates = r'software_security_web_app\src\templates'
ab_path_templates = os.path.abspath(rel_path_templates)
app = Flask(__name__, template_folder=ab_path_templates)

@app.route('/')
def home(): 
    return render_template('home.html')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return home()
    
if __name__ == '__main__':
    app.run(debug=True)