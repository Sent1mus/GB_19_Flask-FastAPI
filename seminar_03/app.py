import os
from flask import Flask, render_template, request
from flask_wtf import CSRFProtect
from models import db, User
from registration_form import RegisterForm
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'put_secretkey_here'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()
        print('OK')


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return "Регистрация прошла успешно"
    return render_template('register.html', form=form)


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
