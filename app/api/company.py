import os

from flask import jsonify, request, flash, url_for, app, current_app
from werkzeug.utils import secure_filename, redirect

import config
from app import db
from app.api.helper import allowed_file
from app.models import TdCompany
from . import api


@api.route('/company/')
def all_customers():
    cp = TdCompany.query.all()
    return jsonify({
        'company': [c.to_json() for c in cp]
    })


@api.route('/company/', methods=['POST'])
def register_customer():

    file = request.files['ci']


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('api.register_customer',
                                filename=filename))

    json_data = request.form.to_dict()

    cp = TdCompany(code=json_data['code'],
                   name_kr=json_data['name_kr'],
                   name_en=json_data['name_en'],
                   name_zh=json_data['name_zh'],
                   registrationNumber=json_data['registrationNumber'],
                   businessRegistrationUrl=json_data['businessRegistrationUrl'],
                   addr_kr=json_data['addr_kr'],
                   addr_en=json_data['addr_en'],
                   addr_zh=json_data['addr_zh'],
                   telephone=json_data['telephone'],
                   fax=json_data['fax'],
                   delegator_kr=json_data['delegator_kr'],
                   delegator_en=json_data['delegator_en'],
                   delegator_zh=json_data['delegator_zh'],
                   state=json_data['state'],
                   dtRegistered=json_data['dtRegistered'],
                   dtModified=json_data['dtModified'],
                   note=json_data['note'],
                   # ci=file,
                   url=json_data['url'],
                   description_kr=json_data['description_kr'],
                   description_en=json_data['description_en'],
                   description_zh=json_data['description_zh'],
                   tntLogoImgUrl=json_data['tntLogoImgUrl'],
                   registrant=json_data['registrant'],
                   modifier=json_data['modifier'])
    cp.ci = file.filename

    print(cp.ci)
    # if 'ci' not in request.files:
    #     flash('No file part')
    #     return redirect(request.url)

    print('test')
    # if user does not select file, browser also
    # submit an empty part without filename
    # if file.filename == '':
    #     flash('No selected file')
    #     return redirect(request.url)
    # print('test1')


    print('test2')
    db.session.add(cp)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/company/<int:id>', methods=['PUT'])
def update_customer(id):
    json_data = request.get_json()
    cp = TdCompany.query.get_or_404(id)

    cp.code = json_data.get('code') or cp.code
    cp.name_kr = json_data.get('name_kr') or cp.name_kr
    cp.name_en = json_data.get('name_en') or cp.name_en
    cp.name_zh = json_data.get('name_zh') or cp.name_zh
    cp.registrationNumber = json_data.get('registrationNumber') or cp.registrationNumber
    cp.businessRegistrationUrl = json_data.get('businessRegistrationUrl') or cp.businessRegistrationUrl
    cp.addr_kr = json_data.get('addr_kr') or cp.addr_kr
    cp.addr_en = json_data.get('addr_en') or cp.addr_en
    cp.addr_zh = json_data.get('addr_zh') or cp.addr_zh
    cp.telephone = json_data.get('telephone') or cp.telephone
    cp.fax = json_data.get('fax') or cp.fax
    cp.delegator_kr = json_data.get('delegator_kr') or cp.delegator_kr
    cp.delegator_en = json_data.get('delegator_en') or cp.delegator_en
    cp.delegator_zh = json_data.get('delegator_zh') or cp.delegator_zh
    cp.state = json_data.get('state') or cp.state
    cp.dtRegistered = json_data.get('dtRegistered') or cp.dtRegistered
    cp.dtModified = json_data.get('dtModified') or cp.dtModified
    cp.note = json_data.get('note') or cp.note
    cp.ci = json_data.get('ci') or cp.ci
    cp.url = json_data.get('url') or cp.url
    cp.description_kr = json_data.get('description_kr') or cp.description_kr
    cp.description_en = json_data.get('description_en') or cp.description_en
    cp.description_zh = json_data.get('description_zh') or cp.description_zh
    cp.tntLogoImgUrl = json_data.get('tntLogoImgUrl') or cp.tntLogoImgUrl
    cp.registrant = json_data.get('registrant') or cp.registrant
    cp.modifier = json_data.get('modifier') or cp.modifier

    db.session.add(cp)
    db.session.commit()

    return jsonify({'result': 'success'})