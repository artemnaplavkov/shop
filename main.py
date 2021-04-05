from data import db_session
from data import users_resource
from data import orders_resource
from data import products_resource
from data import order_details_resource
from data.users import User
from data.orders import Order
from data.orders_resource import order_field
from data.basket import Basket
from data.basket_resource import basket_field
from data.products import Product
from data.products_resource import product_field
from data.order_details import OrderDetails
from data.order_details_resource import order_details_field
from flask import Flask, request, render_template, url_for, redirect, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import reqparse, abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FieldList, FormField
from wtforms import BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired



app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(users_resource.UserListResource, '/api/v2/users')
api.add_resource(users_resource.UserResource, '/api/v2/users/<int:id>')
api.add_resource(orders_resource.OrderListResource, '/api/v2/orders')
api.add_resource(orders_resource.OrderResource,
                 '/api/v2/orders/<int:order_id>')
api.add_resource(products_resource.ProductListResource, '/api/v2/products')
api.add_resource(products_resource.ProductResource,
                 '/api/v2/products/<int:product_id>')
api.add_resource(
    order_details_resource.OrderDetailsListResource, '/api/v2/order_details')
api.add_resource(
    order_details_resource.OrderDetailsResource, '/api/v2/order_details/<int:order_id>/<int:product_id>')

@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


class LoginForm(FlaskForm):
    login = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == form.login.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/orders")
        return render_template('login.html',
                               title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


class RegistrationForm(LoginForm):
    submit = SubmitField('Зарегистрироваться')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data, password=form.password.data)
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('login.html', title='Регистрация', form=form)


@app.route('/orders', methods=['GET'])
def orders():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        orders = db_sess.query(Order).filter(
            Order.user_id == current_user.id)
        return render_template("/orders.html", orders=orders)
    else:
        return redirect("/")

@app.route('/order/<int:order_id>', methods=['GET'])
def order(order_id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        orders = db_sess.query(Order).filter(
            Order.user_id == current_user.id).filter(order_id == Order.order_id)
        print(orders)
        if orders.count() != 1:
            return redirect("/")
        order_details = db_sess.query(OrderDetails).filter(
            order_id == OrderDetails.order_id)
        return render_template("/order_details.html", order_details=order_details)
    else:
        return redirect("/")

def product_choices():
    result = []
    db_sess = db_session.create_session()
    for product in db_sess.query(Product).all():
        result.append((str(product.product_id), product.product_name))
    return result


PRODUCT_CHOICES = []


class ItemForm(FlaskForm):
    product = SelectField('product', choices=PRODUCT_CHOICES)
    quantity = IntegerField('quantity')
    submit = SubmitField()


class OrderForm(FlaskForm):
    items = FieldList(FormField(ItemForm))


@app.route('/buy', methods=['GET'])
def buy():
    if not current_user.is_authenticated:
        return redirect('/')
    form = OrderForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template('buy.html', title='купить', form=form)


@app.route('/basket', methods=['GET'])
def basket():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        basket = db_sess.query(Basket).filter(
            Basket.user_id == current_user.id)
        return render_template("/basket.html", basket=basket)
    else:
        return redirect("/")


def main():
    db_session.global_init("db/shop.sqlite")
    PRODUCT_CHOICES = product_choices()
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()