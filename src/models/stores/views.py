import json

from flask import Blueprint, render_template, request, url_for, redirect

from src.models.stores.store import Store
import src.models.users.decorators as user_decorator

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    store = Store.get_by_id(store_id)
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorator.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store_name = request.form['name']
        store_url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store.name = store_name
        store.url_prefix = store_url_prefix
        store.tag_name = tag_name
        store.query = query
        store.save_to_mongo()

        # return redirect(url_for('.store_page', store_id=store_id))
        return redirect(url_for('.index'))

    return render_template('/stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@user_decorator.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorator.requires_admin_permissions
def create_store():
    if request.method == 'POST':
        store_name = request.form['name']
        store_url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store = Store(store_name, store_url_prefix, tag_name, query)
        store.save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('stores/new_store.html')

