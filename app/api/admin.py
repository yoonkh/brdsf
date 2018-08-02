from flask import jsonify, request, url_for

from flask import jsonify
import json
from app import db
from app.models import TdBlackList, TdRetailer, TdTagVersion, TdAdmin, TsCertReportCount, TlLogin
from . import api
from ..models import *
from .helper import *

@api.route('/admin/customer/')
def all_customers():
    customers = TdCompany.query.all()
    return jsonify({
        'apps': [customer.to_json() for customer in customers]
    })


@api.route('/admin/customer/', methods=['POST'])
def register_customer():
    json_data = request.get_json()
    customer = TdCompany(code=json_data['code'],
                               name_kr=json_data['name_kr'],
                               name_en=json_data['name_en'],
                               name_zh=json_data['name_zh'],
                               registrationNumber=json_data['registrationnumber'],
                               businessRegistrationUrl=json_data['businessregistrationurl'],
                               addr_kr=json_data['addr_kr'],
                               addr_en=json_data['addr_en'],
                               addr_zh=json_data['addr_zh'],
                               telephone=json_data['telephone'],
                               fax=json_data['fax'],
                               delegator_kr=json_data['delegator_kr'],
                               delegator_en=json_data['delegator_en'],
                               delegator_zh=json_data['delegator_zh'],
                               state=json_data['state'],
                               dtRegisetred=json_data['dtregistered'],
                               dtmodified=json_data['dtmodified'],
                               note=json_data['note'],
                               ci=json_data['ci'],
                               url=json_data['url'],
                               description_kr=json_data['description_kr'],
                               description_en=json_data['description_en'],
                               description_zh=json_data['desctiption_zh'],
                               tntLogoImgUrl=json_data['tntlogoimgurl'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = TdCompany.query.get_or_404(id)
    customer.update_app()
    db.session.commit()
    return jsonify(customer.to_json())


@api.route('/admin/icrf-users/')
def all_icrf_users():
   icrfs = TdAdmin.query.all()
   return jsonify({
       'icrf-users': [icrf.to_json() for icrf in icrfs]
   })

@api.route('/admin/icrf-users/', methods=['POST'])
def register_icrf_user():
    json_data = request.get_json()
    icrf = TdAdmin(id=json_data['id'],
                         email=json_data['email'],
                         password_hash=json_data['password'],
                         name=json_data['name'],
                         phone=json_data['phone'],
                         telephone=json_data['telephone'],
                         position=json_data['position'],
                         department=json_data['department'],
                         state=json_data['state'],
                         dtRegistered=json_data['dtregistered'],
                         modifier=json_data['modifier'],
                         dtModified=json_data['dtmodified'],
                         note=json_data['note'])
    db.session.add(icrf)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/icrf-users/<int:id>')
def get_icrf_user(id):
    icrf = TdAdmin.query.get_or_404(id)
    return jsonify(icrf.to_json())


@api.route('/admin/icrf-users/<int:id>', methods=['PUT'])
def update_icrf_user(id):
    icrf = TdAdmin.query.get_or_404(id)
    icrf.update_icrf()
    db.session.commit()
    return jsonify(icrf.to_json())


@api.route('/admin/icrf-users/<int:id>', methods=['DELETE'])
def delete_icrf_user(id):
    icrf = TdAdmin.query.get_or_404(id)
    db.session.delete(icrf)
    db.session.commit()
    return jsonify({'result': 'success'})


# access.query.page 추가해야함
@api.route('/admin/access/')
def get_user_access():
    page = request.args.get('page', 1, type=int)
    pagination = TlLogin.query.paginate(page, per_page=20, error_out=False)
    logins = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_access', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_access', page=page + 1)

    return jsonify({
        'logins': [log.to_json() for log in logins],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


# query.page
@api.route('/admin/blacklist/')
def all_blacklists():
    # blacklists = TdBlackList.query.all()
    # return jsonify({
    #     'blacklists': [blacklist.to_json() for blacklist in blacklists]
    # })
    page = request.args.get('page', 1, type=int)
    pagination = TdBlackList.query.paginate(page, per_page=20, error_out=False)
    blacklists = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.all_blacklists', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.all_blacklists', page=page+1)

    return jsonify({
        'blacklists': [bls.to_json() for bls in blacklists],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/admin/blacklist/', methods=['POST'])
def register_blacklist():
    json_data = request.get_json()
    blacklist = TdBlackList(blType=json_data['blType'],
                            delYN=json_data['delYN'],
                            dtModified=json_data['dtModified'],
                            dtRegistered=json_data['dtRegistered'],
                            modifier=json_data['modifier'],
                            pushToken=json_data['pushToken'],
                            registrant=json_data['registrant'])
    db.session.add(blacklist)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/blacklist/<int:id>', methods=['DELETE'])
def update_blacklist(id):
    blacklist = TdBlackList.query.get_or_404(id)
    db.sesion.delete(blacklist)
    db.session.commit()
    return jsonify(blacklist.to_json())


# over-cert.query.page 추가해야함
@api.route('/admin/over-cert/')
def get_over_cert():
    # over_cert = TsCertReportCount.query.all()
    # return jsonify({
    #     'over_cert': [over.to_json() for over in over_cert]
    # })

    page = request.args.get('page', 1, type=int)
    pagination = TsCertReportCount.query.paginate(page, per_page=20, error_out=False)
    get_over_certs = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_over_cert', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_over_cert', page=page + 1)

    return jsonify({
        'get_over_cert': [get_over_cert.to_json() for get_over_cert in get_over_certs],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


# query.page
@api.route('/admin/randnum/')
def all_randnums():
    randnums = Randnum.query.all()
    return jsonify({
        'randnums': [randnum.to_json() for randnum in randnums]
    })


@api.route('/admin/randnum/', methods=['POST'])
def register_randnum():
    json_data = request.get_json()
    randnum = Randnum(email=json_data['email'],
                      password=json_data['password'],
                      name=json_data['name'])
    db.session.add(randnum)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/randnum/<int:id>', methods=['PUT'])
def update_randnum(id):
    randnum = Randnum.query.get_or_404(id)
    randnum.update_randnum()
    db.session.commit()
    return jsonify(randnum.to_json())


@api.route('/admin/app/')
def all_admin_apps():
    apps = TdAdminApp.query.all()
    return jsonify({
        'apps': [app.to_json() for app in apps]
    })


@api.route('/admin/app/', methods=['POST'])
def register_admin_app():
    json_data = request.get_json()
    app = TdAdminApp(email=json_data['email'],
                     password=json_data['password'],
                     name=json_data['name'])
    db.session.add(app)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/app/<int:id>', methods=['PUT'])
def update_admin_app(id):
    app = TdAdminApp.query.get_or_404(id)
    app.update_app()
    db.session.commit()
    return jsonify(app.to_json())


@api.route('/admin/distributor/')
def all_distributors():
    distributors = TdRetailer.query.all()
    return jsonify({
        'distributors': [distributor.to_json() for distributor in distributors]
    })


@api.route('/admin/distributor/', methods=['POST'])
def register_distributor():
    json_data = request.get_json()
    distributor = TdRetailer(companyCode=json_data['companyCode'],
                             dtModified=json_data['dtModified'],
                             dtRegistered=json_data['dtRegistered'],
                             headerquarterYN=json_data['headerquarterYN'],
                             modifier=json_data['modifier'],
                             name_en=json_data['name_en'],
                             name_kr=json_data['name_kr'],
                             name_zh=json_data['name_zh'],
                             note=json_data['note'],
                             registrant=json_data['registrant'],
                             rtid=json_data['rtid'],
                             state=json_data['state'])
    db.session.add(distributor)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/distributor/<int:id>', methods=['PUT'])
def update_distributor(id):
    distributor = TdRetailer.query.get_or_404(id)
    distributor.update_distributor()
    db.session.commit()
    return jsonify(distributor.to_json())


@api.route('/admin/distributor/<int:id>', methods=['DELETE'])
def delete_distributor(id):
    distributor = TdRetailer.query.get_or_404(id)
    db.session.delete(distributor)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/tag-type/')
def all_tag_types():
    tag_types = TdTagVersion.query.all()
    return jsonify({
        'tag_type': [tag_type.to_json() for tag_type in tag_types]
    })


@api.route('/admin/tag-type/', methods=['POST'])
def register_tag_type():
    json_data = request.get_json()
    tag_type = TdTagVersion(description=json_data['description'],
                            dtModified=json_data['dtModified'],
                            dtRegistered=json_data['dtRegistered'],
                            height=json_data['height'],
                            modifier=json_data['modifier'],
                            name_en=json_data['name_en'],
                            name_kr=json_data['name_kr'],
                            name_zh=json_data['name_zh'],
                            note=json_data['note'],
                            registrant=json_data['registrant'],
                            state=json_data['state'],
                            type=json_data['type'],
                            version=json_data['version'],
                            width=json_data['width'])
    db.session.add(tag_type)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/tag-type/<int:id>', methods=['PUT'])
def update_tag_type(id):
    tag_type = TdTagVersion.query.get_or_404(id)
    tag_type.update_distributor()
    db.session.commit()
    return jsonify(tag_type.to_json())


@api.route('/admin/tag-type/<int:id>', methods=['DELETE'])
def delete_tag_type(id):
    tag_type = TdTagVersion.query.get_or_404(id)
    db.session.delete(tag_type)
    db.session.commit()
    return jsonify({'result': 'success'})