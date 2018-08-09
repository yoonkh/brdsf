from flask import jsonify, request, current_app, url_for
from sqlalchemy import and_

from app.api.helper import date_range, page_and_search
from app.models import ThCertification
from . import api


# query.page
@api.route('/prod-cert/')
def all_prods():
    start, end = date_range()
    print(start, end)
    page, search = page_and_search()

    # 날짜 range and order
    certs = ThCertification.query.filter(ThCertification.dtCertificate.between(start, end)) \
            .filter(ThCertification.companyCode.like('%' + search + '%')) \
            .filter(ThCertification.result.like('%' + search + '%')) \
            .filter(ThCertification.tagType.like('%' + search + '%')) \
            .filter(ThCertification.osType.like('%' + search + '%')).order_by(ThCertification.dtCertificate.desc())

    # 각종 조건문 필터
    # 페이지네이션
    certs = certs.paginate(page=int(page), per_page=20, error_out=False).items
    # return jsonify({'total': certs.total, 'certs': [cert.to_json() for cert in certs]})
    return jsonify({'certs': [cert.to_json() for cert in certs]})


@api.route('/prod-cert/<int:id>')
def get_prod(id):
    prod = ThCertification.query.get_or_404(id)
    return jsonify(prod.to_json())
