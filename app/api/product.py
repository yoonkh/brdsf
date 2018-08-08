from flask import jsonify, request, current_app, url_for

from app.models import ThCertification
from . import api


# query.page
@api.route('/prod-cert/')
def all_prods():
    # page = request.args.get('page', 1, type=int)
    paginations = ThCertification.query.limit(10).all()
    # prods = pagination.items
    # prev = None
    # if pagination.has_prev:
    #     prev = url_for('api.all_prods', page=page-1)
    # next = None
    # if pagination.has_next:
    #     next = url_for('api.all_prods', page=page+1)

    return jsonify({
        'prods': [pagination.to_json for pagination in paginations]
        #     [prod.to_json() for prod in prods],
        # 'prev': prev,
        # 'next': next,
        # 'count': pagination.total
    })


@api.route('/prod-cert/<int:id>')
def get_prod(id):
    prod = ThCertification.query.get_or_404(id)
    return jsonify(prod.to_json())
