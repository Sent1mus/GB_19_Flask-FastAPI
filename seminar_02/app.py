from flask import Flask, request, make_response, render_template, redirect
from markupsafe import escape

app = Flask(__name__)


@app.route('/index/', methods=['GET', 'POST'])
def index():
    username = request.cookies.get('username')
    if request.method == 'POST':
        response = make_response(redirect('/authorisation/'))
        response.delete_cookie('username')
        response.delete_cookie('email')
        return response
    return render_template('index.html', username=username)


@app.route('/authorisation/', methods=['GET', 'POST'])
def authorisation():
    if request.method == 'POST':
        username = escape(request.form.get('auth_username'))
        email = escape(request.form.get('auth_email'))
        response = make_response(redirect('/index/'))
        response.set_cookie('username', username)
        response.set_cookie('email', email)
        return response
    return render_template('authorisation.html')


if __name__ == '__main__':
    app.run(debug=True)
