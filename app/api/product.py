from flask import jsonify
from . import api


# query.page
@api.route('/prod-cert/')
def all_prods():
    prods = Product.query.all()
    return jsonify({
        'users': [prod.to_json() for prod in prods]
    })


@api.route('/prod-cert/<int:id>')
def get_prod(id):
    prod = Product.query.get_or_404(id)
    return jsonify(prod.to_json())
