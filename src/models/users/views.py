from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorator

from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    # print(request.methods)
    # print(request.form['email'])
    # print(request.form['hashed'])
    if request.method == 'POST':
        # Check login is valid
        email = request.form['email']
        # password = request.form['hashed']
        password = request.form['password']
        try:
            if User.login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".alert_user"))
        # except UserErrors.UserNotExistsError as e:
        #     return e.message
        # except UserErrors.IncorrectPasswordError as e:
        #     return e.message
        except UserErrors.UserError as e:
            return e.message

    return render_template("/users/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        # password = request.form['hashed']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".alert_user"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("/users/register.html")


@user_blueprint.route('/alert')
@user_decorator.requires_login
def alert_user():
    user = User.find_by_email(session['email'])
    # print(user)
    alerts = user.get_alerts()
    # print(alerts)
    return render_template('users/alerts.html', alerts=alerts)
    # return "This is the alerts page."


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return  redirect(url_for('home'))


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass