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
    per_page = request.args.get('perPage', 10)

    query_data = request.args
    companycode = query_data.get('companycode', '')
    result = query_data.get('result', '')
    tag = query_data.get('tag', '')
    os = query_data.get('os', '')


    # 날짜 range and order
    certs = ThCertification.query.filter(ThCertification.dtCertificate.between(start, end)) \

    if companycode:
        certs = certs.filter_by(companyCode=companycode)

    if result:
        certs = certs.filter_by(result=result)

    if tag:
        certs = certs.filter_by(tagType=tag)

    if os:
        certs = certs.filter_by(osType=os)

    certs.order_by(ThCertification.dtCertificate.desc())

    # 페이지네이션
    pagination = certs.paginate(page=int(page), per_page=int(per_page), error_out=False)
    certs = pagination.items
    # return jsonify({'total': certs.total, 'certs': [cert.to_json() for cert in certs]})
    return jsonify({'total': pagination.total, 'certs': [cert.to_json() for cert in certs]})


@api.route('/prod-cert/<int:id>')
def get_prod(id):
    prod = ThCertification.query.get_or_404(id)
    return jsonify(prod.to_json())


# @api.route('/prod-certs/')
# def all_prods():
#     start, end = date_range()
#     print(start, end)
#     page, search = page_and_search()
#     per_page = request.args.get('perPage', 10)
#
#     # 날짜 range and order
#     certs = ThCertification.query.filter(ThCertification.dtCertificate.between(start, end)) \
#             .filter(ThCertification.companyCode.like('%' + search + '%')) \
#             .filter(ThCertification.result.like('%' + search + '%')) \
#             .filter(ThCertification.tagType.like('%' + search + '%')) \
#             .filter(ThCertification.osType.like('%' + search + '%')) \
#             .filter(ThCertification) \
#             .order_by(ThCertification.dtCertificate.desc())
#
#     # 페이지네이션
#     # return jsonify({'total': certs.total, 'certs': [cert.to_json() for cert in certs]})
#     return jsonify({'total': certs.total, 'certs': [cert.to_json() for cert in certs]})
