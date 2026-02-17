from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home(): 
    return '<h1>Welcome to Home</h1>'


@app.route('/login')
def login(): 
    return render_template('login_page.html')


if __name__ == '__main__':
    app.run(debug=True)