from data import db_session
from data import users_resource
from data.users import User
from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired



app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(users_resource.UserListResource, '/api/v2/users')
api.add_resource(users_resource.UserResource, '/api/v2/users/<int:id>')


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


class LoginForm(FlaskForm):
    login = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    

@app.route('/', methods=['GET'])
def index():
    return "hello shop"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/shop.sqlite")
    
    
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()