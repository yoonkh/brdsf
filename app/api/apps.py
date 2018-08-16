from flask import jsonify, request

from flask import jsonify
from ..models import *
from app import db
from app.models import TdApp
from . import api


# query.page
@api.route('/apps/', methods=['GET'])
def all_apps():
    apps = TdApp.query.all()
    return jsonify({
        'apps': [app.to_json() for app in apps]
    })


@api.route('/apps/', methods=['POST'])
def register_app():
    json_data = request.get_json()

    app = TdApp(code=json_data['code'],
                companyCode=json_data['companyCode'],
                registrant=json_data['registrant'],
                name_kr=json_data['name_kr'],
                name_en=json_data['name_en'],
                name_zh=json_data['name_zh'],
                version=json_data['version'],
                type=json_data['type'],
                tagType=json_data['tagType'],
                dtRegistered=json_data['dtRegistered'],
                note=json_data['note'],
                dtPublished=json_data['dtPublished'],
                attachedPath=json_data['attachedPath'],
                osType=json_data['osType'],
                modifier=json_data['modifier'],
                dtModified=json_data['dtModified'],
                description=json_data['description'],
                limitCertHour=json_data['limitCertHour'],
                limitCertCnt=json_data['limitCertCnt'],
                updateUrl=json_data['updateUrl'])
    app.state = 'Enable'
    db.session.add(app)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/apps/<int:id>')
def get_app(id):
    app = TdApp.query.get_or_404(id)
    return jsonify(app.to_json())


@api.route('/apps/<int:id>', methods=['PUT'])
def update_app(id):
    json_data = request.get_json()
    app = TdApp.query.get_or_404(id)

    app.code = json_data.get('code') or app.code
    app.companyCode = json_data.get('companyCode') or app.companyCode
    app.registrant = json_data.get('registrant') or app.registrant
    app.name_kr = json_data.get('name_kr') or app.name_kr
    app.name_en = json_data.get('name_en') or app.name_en
    app.name_zh = json_data.get('name_zh') or app.name_zh
    app.version = json_data.get('version') or app.version
    app.type = json_data.get('type') or app.type
    app.tagType = json_data.get('tagType') or app.tagType
    app.dtRegistered = json_data.get('dtRegistered') or app.dtRegistered
    app.note = json_data.get('note') or app.note
    app.dtPublished = json_data.get('dtPublished') or app.dtPublished
    app.attachedPath = json_data.get('attachedPath') or app.attachedPath
    app.osType = json_data.get('osType') or app.osType
    app.modifier = json_data.get('modifier') or app.modifier
    app.dtModified = json_data.get('dtModified') or app.dtModified
    app.description = json_data.get('description') or app.description
    app.limitCertHour = json_data.get('limitCertHour') or app.limitCertHour
    app.limitCertCnt = json_data.get('limitCertCnt') or app.limitCertCnt
    app.updateUrl = json_data.get('updateUrl') or app.updateUrl
    app.state = json_data.get('state') or app.state

    db.session.add(app)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/apps/<int:id>', methods=['DELETE'])
def delete_app(id):
    app = TdApp.query.get_or_404(id)
    db.session.delete(app)
    db.session.commit()
    return jsonify({'result': 'success'})