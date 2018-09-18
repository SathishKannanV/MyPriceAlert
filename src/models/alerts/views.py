from flask import Blueprint, render_template, request, session, url_for, redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorator

alert_blueprint = Blueprint('alerts', __name__)

# @alert_blueprint.route('/')
# def index():
#     return "You are on Alert page!"

@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorator.requires_login
def create_alert():
    if request.method == 'POST':
        item_name = request.form['name']
        item_url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(item_name, item_url)
        # item.load_price()
        item.save_to_mongo()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() # This already saves to mongoDB

        return redirect(url_for('users.alert_user'))

    return render_template('alerts/create_alert.html')



@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorator.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('users.alert_user'))

    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorator.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.alert_user'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorator.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.alert_user'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorator.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.alert_user'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorator.requires_login
def get_alert_page(alert_id):
    # print("Alert id: " + alert_id)
    alert = Alert.find_by_id(alert_id)
    # print(alert)
    return render_template('alerts/alert.html', alert=alert)

# @alert_blueprint.route('/for_user/<string:alert_id>')
# def get_alerts_for_user(alert_id):
#     pass


@alert_blueprint.route('/check_price/<string:alert_id>')
@user_decorator.requires_login
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    # alert = Alert.find_by_id(alert_id)
    # alert.load_item_price()
    # print(alert)
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
