from flask import jsonify, request, current_app, url_for

from app import db
from app.api.decorators import accessible_oneself
from app.api.errors import forbidden
from . import api
from ..models import TdAccount


@api.route('/users/')
def all_users():
    users = TdAccount.query.all()
    return jsonify({
        'users': [user.to_json() for user in users]
    })


@api.route('/users/', methods=['POST'])
def register_user():
    json_data = request.get_json()
    user = TdAccount(companyCode=json_data['companycode'],
                     email=json_data['email'],
                     password_hash=json_data['password'],
                     name_kr=json_data['name_kr'],
                     name_en=json_data['name_en'],
                     name_ch=json_data['name_ch'],
                     phone=json_data['phone'],
                     telephone=json_data['telephone'],
                     fax=json_data['fax'],
                     position=json_data['position'],
                     department=json_data['department'],
                     state=json_data['state'],
                     registrant=json_data['registrant'],
                     # dtRegistered=json_data['dtregistered'],
                     # dtModified=json_data['dtmodified'],
                     # dtLastConnected=json_data['dtlastconnected'],
                     note=json_data['note'])
    db.session.add(user)
    db.session.commit()
    # return jsonify({'result': 'success'})
    return jsonify({
        'users': user.to_json()
    })


@api.route('/users/<int:id>')
def get_user(id):
    user = TdAccount.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>', methods=['PUT'])
@accessible_oneself()
def update_user(id):
    json_data = request.get_json()
    role = json_data['role']
    pass


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = TdAccount.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/users/<int:id>/pw-reset', methods=['PUT'])
@accessible_oneself()
def reset_password(id):
    # user = TdAccount.query.get_or_404(id)
    # password = user.reset_password()
    # db.session.commit()
    # return jsonify({'result': 'success', 'password': password})
    user = g.user
    passwords = request.get_json()
    old_password = passwords.get('old_password')
    new_password = passwords.get('new_password')

    if not user.verify_password(old_password):
        return forbidden('Invalid credentials')
    else:
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': 'success'})


@api.route('/users/<int:id>/change-role/', methods=['PUT'])
def change_role(id):
    user = TdAccount.query.get_or_404(id)
    role = request.args.get('role', user.role.name)
    user.change_role(role)
    db.session.commit()
    return jsonify({'result': 'success'})