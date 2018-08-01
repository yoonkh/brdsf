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
    json_data = TdApp.get_json()

    app = TdApp(code=json_data['code'],
                name_kr=json_data['name_kr'],
                name_en=json_data['name_en'],
                name_zh=json_data['name_zh'],
                version=json_data['version'],
                type=json_data['type'],
                tagType=json_data['tagtype'],
                dtRegistered=json_data['dtregistered'],
                note=json_data['note'],
                dtPublished=json_data['dtpublished'],
                attachedPath=json_data['attachedpath'],
                osType=json_data['ostype'],
                modifier=json_data['modifier'],
                description=json_data['description'],
                limitCertHour=json_data['limitcerthour'],
                limitCertCnt=json_data['limitcertcnt'],
                updateUrl=json_data['updateurl'])
    db.session.add(app)
    db.session.commit()
    return jsonify({'result': 'success'})


@api.route('/apps/<int:id>')
def get_app(id):
    app = TdApp.query.get_or_404(id)
    return jsonify(app.to_json())


@api.route('/apps/<int:id>', methods=['PUT'])
def update_app(id):
    app = TdApp.query.get_or_404(id)
    app.update_app()
    db.session.commit()
    return jsonify(app.to_json())


@api.route('/apps/<int:id>', methods=['DELETE'])
def delete_app(id):
    app = TdApp.query.get_or_404(id)
    db.session.delete(app)
    db.session.commit()
    return jsonify({'result': 'success'})