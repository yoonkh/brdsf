from flask import jsonify, request

from app import db
from app.models import TdCompany
from . import api


@api.route('/company/')
def all_customers():
    customers = TdCompany.query.all()
    return jsonify({
        'customers': [customer.to_json() for customer in customers]
    })


@api.route('/company/', methods=['POST'])
def register_customer():
    json_data = request.get_json()
    customer = TdCompany(code=json_data['code'],
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
                         ci=json_data['ci'],
                         url=json_data['url'],
                         description_kr=json_data['description_kr'],
                         description_en=json_data['description_en'],
                         description_zh=json_data['description_zh'],
                         tntLogoImgUrl=json_data['tntLogoImgUrl'],
                         registrant=json_data['registrant'],
                         modifier=json_data['modifier'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/company/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = TdCompany.query.get_or_404(id)
    customer.update_app()
    db.session.commit()
    return jsonify(customer.to_json())