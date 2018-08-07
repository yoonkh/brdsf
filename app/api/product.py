from flask import jsonify, request, current_app, url_for

from app.api.helper import date_range
from app.models import ThCertification
from . import api


# query.page
@api.route('/prod-cert/')
def all_prods():
    start, end = date_range()
    dates = ThCertification.query.filter(ThCertification.dtCertificate.between(start, end)).order_by(ThCertification.dtCertificate.asc()).all()
    query_data = request.args
    page, search = query_data.get('page', 1), query_data.get('query', '')
    if len(search) > 1:
        certs = dates.query.filter((ThCertification.id.ilike('%' + search + '%')))
    else:
        certs = ThCertification.query
    certs = certs.order_by(ThCertification.idx.desc()).paginate(page=int(page), per_page=20, error_out=False)
    return jsonify({'total': certs.total, 'certs': [cert.to_json() for cert in certs.items]})


@api.route('/prod-cert/<int:id>')
def get_prod(id):
    prod = ThCertification.query.get_or_404(id)
    return jsonify(prod.to_json())
