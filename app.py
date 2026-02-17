from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login(): 
    return render_template('login_page.html')


if __name__ == '__main__':
    app.run(debug=True)