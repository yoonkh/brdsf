from app.api.helper import date_range, page_and_search
from ..models import *

from flask import jsonify, request, current_app, url_for, g

from app import db
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
                     password=json_data['password'],
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
def reset_password(id):
    # json_data = request.get_json()
    # user = TdAccount.query.get_or_404(id)
    # old_pwd = json_data.get('old_pwd')
    # new_pwd = json_data.get('new_pwd')
    # print(old_pwd)
    # if old_pwd == user.pwd:
    #     user.pwd = new_pwd
    #     db.session.add(user)
    #     db.session.commit()
    #     response = {'result': 'success'}
    # else:
    #     response = {'result': 'fail'}
    # return jsonify({'result': response, 'new_password': user.pwd})
    user = TdAccount.query.get_or_404(id)
    password = user.reset_password()
    db.session.commit()
    return jsonify({'result': 'success', 'password': password})


@api.route('/admin/users/<int:id>/change-role/', methods=['PUT'])
def change_role(id):
    json_data = request.get_json()
    user = TdAccount.query.get_or_404(id)
    user.role = json_data['role']
    db.session.add(user)
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
    json_data = request.get_json()
    icrf = TdAdmin.query.get_or_404(id)

    icrf.id = json_data.get('id') or icrf.id
    icrf.pwd = json_data.get('pwd') or icrf.pwd
    icrf.email = json_data.get('email') or icrf.email
    icrf.department = json_data.get('department') or icrf.department
    icrf.dtLastConnected = json_data.get('dtLastConnected') or icrf.dtLastConnected
    icrf.dtModified = json_data.get('dtModified') or icrf.dtModified
    icrf.dtRegistered = json_data.get('dtRegistered') or icrf.dtRegistered
    icrf.failCount = json_data.get('failCount') or icrf.failCount
    icrf.modifier = json_data.get('modifier') or icrf.modifier
    icrf.name = json_data.get('name') or icrf.name
    icrf.note = json_data.get('note') or icrf.note
    icrf.phone = json_data.get('phone') or icrf.phone
    icrf.position = json_data.get('position') or icrf.position
    icrf.registrant = json_data.get('registrant') or icrf.registrant
    icrf.role = json_data.get('role') or icrf.role
    icrf.state = json_data.get('state') or icrf.state
    icrf.telephone = json_data.get('telephone') or icrf.telephone

    db.session.add(icrf)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/admin/icrf-users/<int:id>', methods=['DELETE'])
def delete_icrf_user(id):
    icrf = TdAdmin.query.get_or_404(id)
    db.session.delete(icrf)
    db.session.commit()
    return jsonify({'result': 'success'})


# access.query.page 추가해야함
@api.route('/admin/access/')
def get_user_access():
    # page = request.args.get('page', 1, type=int)
    # pagination = TlLogin.query.paginate(page, per_page=20, error_out=False)
    # logins = pagination.items
    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('api.get_user_access', page=page - 1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('api.get_user_access', page=page + 1)
    #
    # return jsonify({
    #     'logins': [log.to_json() for log in logins],
    #     'prev': prev,
    #     'next': next,
    #     'count': pagination.total
    # })
    start, end = date_range()
    dates = TlLogin.query.filter(TlLogin.dtAttempted.between(start, end)).order_by(TlLogin.dtAttempted.asc())
    query_data = request.args
    page, search = query_data.get('page', 1), query_data.get('query', '')
    if len(search) > 1:
        logs = dates.filter((TlLogin.id.like('%' + search + '%')))
    else:
        logs = dates
    logs = logs.order_by(TlLogin.idx.desc()).paginate(page=int(page), per_page=20, error_out=False)
    return jsonify({'total': logs.total, 'logs': [log.to_json() for log in logs.items]})


# query.page
@api.route('/admin/blacklist/')
def all_blacklists():
    blacklists = TdBlackList.query.all()
    return jsonify({
        'blacklists': [blacklist.to_json() for blacklist in blacklists]
    })
    # page = request.args.get('page', 1, type=int)
    # pagination = TdBlackList.query.paginate(page, per_page=20, error_out=False)
    # blacklists = pagination.items
    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('api.all_blacklists', page=page-1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('api.all_blacklists', page=page+1)
    #
    # return jsonify({
    #     'blacklists': [bls.to_json() for bls in blacklists],
    #     'prev': prev,
    #     'next': next,
    #     'count': pagination.total
    # })


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
    # page = request.args.get('page', 1, type=int)
    # pagination = TsCertReportCount.query.paginate(page, per_page=20, error_out=False)
    # get_over_certs = pagination.items
    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('api.get_over_cert', page=page - 1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('api.get_over_cert', page=page + 1)
    #
    # return jsonify({
    #     'get_over_cert': [get_over_cert.to_json() for get_over_cert in get_over_certs],
    #     'prev': prev,
    #     'next': next,
    #     'count': pagination.total
    # })
    start, end = date_range()
    dates = TdDevice.query.filter(TdDevice.dtRegistered.between(start, end)).order_by(TdDevice.dtRegistered.asc())
    page, search = page_and_search()
    if len(search) > 1:
        certs = dates.filter((TdDevice.pushToken.ilike('%' + search + '%')))
        # (TsCertReportCount.idx.has(TdAdminApp.pushToken.ilike('%' + search + '%'))))
    else:
        certs = dates
    certs = certs.order_by(TdDevice.idx.desc()).paginate(page=int(page), per_page=20, error_out=False)
    return jsonify({'total': certs.total, 'certs': [cert.to_json() for cert in certs.items]})


# query.page
@api.route('/admin/randnum/')
def all_randnums():
    # page = request.args.get('page', 1, type=int)
    # pagination = TdRandomMnge.query.paginate(page, per_page=20, error_out=False)
    # TdRandomMnges = pagination.items
    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('api.all_randnums', page=page - 1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('api.all_randnums', page=page + 1)
    #
    # return jsonify({
    #     'randnum': [rn.to_json() for rn in TdRandomMnges],
    #     'prev': prev,
    #     'next': next,
    #     'count': pagination.total
    # })
    query_data = request.args
    page, search = query_data.get('page', 1), query_data.get('query', '')
    if len(search) > 1:
        rans = TdRandomMnge.query.filter((TdRandomMnge.tagCode.like('%' + search + '%')))
        # (TlLogin.id.has(TdAccount.id.ilike('%' + search + '%')))))
    else:
        rans = TdRandomMnge.query
    rans = rans.order_by(TdRandomMnge.idx.desc()).paginate(page=int(page), per_page=20, error_out=False)
    return jsonify({'total': rans.total, 'rans': [ran.to_json() for ran in rans.items]})


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
    json_data = request.get_json()
    randnum = TdRandomMnge.query.get_or_404(id)

    randnum.companyCode = json_data.get('companyCode') or randnum.companyCode
    randnum.delYN = json_data.get('delYN') or randnum.delYN
    randnum.dtExpired = json_data.get('dtExpired') or randnum.dtExpired
    randnum.dtModified = json_data.get('dtModified') or randnum.dtModified
    randnum.dtPrinted = json_data.get('dtPrinted') or randnum.dtPrinted
    randnum.dtRegistered = json_data.get('dtRegistered') or randnum.dtRegistered
    randnum.dtShipping = json_data.get('dtShipping') or randnum.dtShipping
    randnum.memo = json_data.get('memo') or randnum.memo
    randnum.modifier = json_data.get('modifier') or randnum.modifier
    randnum.registrant = json_data.get('registrant') or randnum.registrant
    randnum.retailerID = json_data.get('retailerID') or randnum.retailerID
    randnum.tableNum = json_data.get('tableNum') or randnum.tableNum
    randnum.tagCode = json_data.get('tagCode') or randnum.tagCode
    randnum.ticketCnt = json_data.get('ticketCnt') or randnum.ticketCnt
    randnum.ticketEndIdx = json_data.get('ticketEndIdx') or randnum.ticketEndIdx
    randnum.ticketFileName = json_data.get('ticketFileName') or randnum.ticketFileName
    randnum.ticketListState = json_data.get('ticketListState') or randnum.ticketListState
    randnum.ticketStartIdx = json_data.get('ticketStartIdx') or randnum.ticketStartIdx

    db.session.add(randnum)
    db.session.commit()
    return jsonify({'result': 'success'})


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
    json_data = request.get_json()
    app = TdAdminApp.query.get_or_404(id)

    app.companyName = json_data.get('companyName') or app.companyName
    app.contact = json_data.get('contact') or app.contact
    app.dtModified = json_data.get('dtModified') or app.dtModified
    app.dtRegistered = json_data.get('dtRegistered') or app.dtRegistered
    app.modifier = json_data.get('modifier') or app.modifier
    app.name = json_data.get('name') or app.name
    app.pushToken = json_data.get('pushToken') or app.pushToken
    app.state = json_data.get('state') or app.state

    db.session.add(app)
    db.session.commit()
    return jsonify({'result': 'success'})


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
    json_data =request.get_json()
    distributor = TdRetailer.query.get_or_404(id)

    distributor.companyCode = json_data.get('companyCode') or distributor.companyCode
    distributor.dtModified = json_data.get('dtModified') or distributor.dtModified
    distributor.dtRegistered = json_data.get('dtRegistered') or distributor.dtRegistered
    distributor.headerquarterYN = json_data.get('headerquarterYN') or distributor.headerquarterYN
    distributor.modifier = json_data.get('modifier') or distributor.modifier
    distributor.name_en = json_data.get('name_en') or distributor.name_en
    distributor.name_kr = json_data.get('name_kr') or distributor.name_kr
    distributor.name_zh = json_data.get('name_zh') or distributor.name_zh
    distributor.note = json_data.get('note') or distributor.note
    distributor.registrant = json_data.get('registrant') or distributor.registrant
    distributor.rtid = json_data.get('rtid') or distributor.rtid
    distributor.state = json_data.get('state') or distributor.state

    db.session.add(distributor)
    db.session.commit()
    return jsonify({'result': 'success'})


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
    json_data = request.get_json()
    tag_type = TdTagVersion.query.get_or_404(id)

    tag_type.description = json_data.get('description') or tag_type.description
    tag_type.dtModified = json_data.get('dtModified') or tag_type.dtModified
    tag_type.dtRegistered = json_data.get('dtRegistered') or tag_type.dtRegistered
    tag_type.height = json_data.get('height') or tag_type.height
    tag_type.modifier = json_data.get('modifier') or tag_type.modifier
    tag_type.name_en = json_data.get('name_en') or tag_type.name_en
    tag_type.name_kr = json_data.get('name_kr') or tag_type.name_kr
    tag_type.name_zh = json_data.get('name_zh') or tag_type.name_zh
    tag_type.note = json_data.get('note') or tag_type.note
    tag_type.registrant = json_data.get('registrant') or tag_type.registrant
    tag_type.state = json_data.get('state') or tag_type.state
    tag_type.type = json_data.get('type') or tag_type.type
    tag_type.version = json_data.get('version') or tag_type.version
    tag_type.width = json_data.get('width') or tag_type.width

    db.session.add(tag_type)
    db.session.commit()

    return jsonify({'result': 'success'})


@api.route('/admin/tag-type/<int:id>', methods=['DELETE'])
def delete_tag_type(id):
    tag_type = TdTagVersion.query.get_or_404(id)
    db.session.delete(tag_type)
    db.session.commit()
    return jsonify({'result': 'success'})