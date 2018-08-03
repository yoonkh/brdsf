from ..models import *

from flask import jsonify, request, current_app, url_for

from app import db
from app.api.decorators import accessible_oneself
from app.api.errors import forbidden
from . import api
from ..models import TdAccount


@api.route('/admin/users/')
def all_users():
    users = TdAccount.query.all()
    return jsonify({
        'users': [user.to_json() for user in users]
    })


@api.route('/admin/users/', methods=['POST'])
def register_user():
    json_data = request.get_json()
    user = TdAccount(id=json_data['id'],
                     pwd=json_data['pwd'],
                     email=json_data['email'],
                     name_kr=json_data['name_kr'],
                     name_en=json_data['name_en'],
                     name_zh=json_data['name_zh'],
                     phone=json_data['phone'],
                     telephone=json_data['telephone'],
                     fax=json_data['fax'],
                     position=json_data['position'],
                     companyCode=json_data['companyCode'],
                     role=json_data['role'],
                     department=json_data['department'],
                     state=json_data['state'],
                     registrant=json_data['registrant'],
                     dtRegistered=json_data['dtRegistered'],
                     modifier=json_data['modifier'],
                     dtModified=json_data['dtModified'],
                     dtLastConnected=json_data['dtLastConnected'],
                     note=json_data['note'],
                     failCount=json_data['failCount'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/users/<int:id>')
def get_user(id):
    user = TdAccount.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/admin/users/<int:id>', methods=['PUT'])
def update_user(id):
    json_data = request.get_json()
    user = TdAccount.query.get_or_404(id)

    user.id = json_data.get('id') or user.id
    user.pwd = json_data.get('pwd') or user.pwd
    user.email = json_data.get('email') or user.email
    user.name_kr = json_data.get('name_kr') or user.name_kr
    user.name_en = json_data.get('name_en') or user.name_en
    user.name_zh = json_data.get('name_zh') or user.name_zh
    user.phone = json_data.get('phone') or user.phone
    user.telephone = json_data.get('telephone') or user.telephone
    user.fax = json_data.get('fax') or user.fax
    user.position = json_data.get('position') or user.position
    user.companyCode = json_data.get('companyCode') or user.companyCode
    user.role = json_data.get('role') or user.role
    user.department = json_data.get('department') or user.department
    user.state = json_data.get('state') or user.state
    user.registrant = json_data.get('registrant') or user.registrant
    user.dtRegistered = json_data.get('dtRegistered') or user.dtRegistered
    user.modifier = json_data.get('modifier') or user.modifier
    user.dtModified = json_data.get('dtModified') or user.dtModified
    user.dtLastConnected = json_data.get('dtLastConnected') or user.dtLastConnected
    user.note = json_data.get('note') or user.note
    user.failCount = json_data.get('failCount') or user.failCount

    db.session.add(user)
    db.session.commit()

    print(user)
    return jsonify({'result': 'success'})


@api.route('/admin/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = TdAccount.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/users/<int:id>/pw-reset', methods=['PUT'])
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
        user.pwd = new_password
        db.session.add(user)
        db.session.commit()
        return jsonify({'result': 'success'})


@api.route('/admin/users/<int:id>/change-role/', methods=['PUT'])
def change_role(id):
    user = TdAccount.query.get_or_404(id)
    role = request.args.get('role', user.role.name)
    user.change_role(role)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/icrf-users/')
def all_icrf_users():
   icrfs = TdAdmin.query.all()
   return jsonify({
       'icrf-users': [icrf.to_json() for icrf in icrfs]
   })

@api.route('/admin/icrf-users/', methods=['POST'])
def register_icrf_user():
    json_data = request.get_json()
    icrf = TdAdmin(department=json_data['department'],
                   dtLastConnected=json_data['dtLastConnected'],
                   dtModified=json_data['dtModified'],
                   dtRegistered=json_data['dtRegistered'],
                   email=json_data['email'],
                   failCount=json_data['failCount'],
                   id=json_data['id'],
                   modifier=json_data['modifier'],
                   name=json_data['name'],
                   note=json_data['note'],
                   phone=json_data['phone'],
                   position=json_data['position'],
                   pwd=json_data['pwd'],
                   registrant=json_data['registrant'],
                   role=json_data['role'],
                   state=json_data['state'],
                   telephone=json_data['telephone'])
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
    # randnums = TdRandomMnge.query.all()
    # return jsonify({
    #     'randnums': [randnum.to_json() for randnum in randnums]
    # })
    page = request.args.get('page', 1, type=int)
    pagination = TdRandomMnge.query.paginate(page, per_page=20, error_out=False)
    TdRandomMnges = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.all_randnums', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.all_randnums', page=page + 1)

    return jsonify({
        'randnum': [rn.to_json() for rn in TdRandomMnges],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/admin/randnum/', methods=['POST'])
def register_randnum():
    json_data = request.get_json()
    randnum = TdRandomMnge(companyCode=json_data['companyCode'],
                           delYN=json_data['delYN'],
                           dtExpired=json_data['dtExpired'],
                           dtModified=json_data['dtModified'],
                           dtRegistered=json_data['dtRegistered'],
                           dtPrinted=json_data['dtPrinted'],
                           dtShipping=json_data['dtShipping'],
                           memo=json_data['memo'],
                           modifier=json_data['modifier'],
                           registrant=json_data['registrant'],
                           retailerID=json_data['retailerID'],
                           tableNum=json_data['tableNum'],
                           tagCode=json_data['tagCode'],
                           ticketCnt=json_data['ticketCnt'],
                           ticketEndIdx=json_data['ticketEndIdx'],
                           ticketFileName=json_data['ticketFileName'],
                           ticketListState=json_data['ticketListState'],
                           ticketStartIdx=json_data['ticketStartIdx'])
    db.session.add(randnum)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/randnum/<int:id>', methods=['PUT'])
def update_randnum(id):
    randnum = TdRandomMnge.query.get_or_404(id)
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
    app = TdAdminApp(companyName=json_data['companyName'],
                     contact=json_data['contact'],
                     dtModified=json_data['dtModified'],
                     dtRegistered=json_data['dtRegistered'],
                     modifier=json_data['modifier'],
                     name=json_data['name'],
                     pushToken=json_data['pushToken'],
                     state=json_data['state'])
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