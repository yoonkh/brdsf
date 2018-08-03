from flask import jsonify, request, current_app, url_for
from app import db
from app.api.decorators import accessible_oneself
from app.api.errors import forbidden
from . import api
from ..models import TsCertReportCount, ThCertification, ThReport
from .helper import cert_date_range, static_date_range
from itertools import  groupby


@api.route('/dashboard1/')
def real_time_status():
    start, end = cert_date_range()
    status = ThCertification.query.filter(ThCertification.dtCertificate.between(start, end)).order_by(ThCertification.dtCertificate.desc()).all()
    g_status = groupby(status, lambda s: s.dtCertificate.strftime('%Y-%m-%d %H:%M'))
    report = ThReport.query.filter(ThReport.dtCreated.between(start, end)).order_by(ThReport.dtCreated.desc()).all()
    g_report = groupby(report, lambda s: s.dtCreated.strftime('%Y-%m-%d %H:%M'))

    real_time_s = dict()
    for (minute, group) in g_status:
        m = minute
        c_count = 0
        g_count = 0
        for g in group:
            if g.result == 'Counterfeit':
                c_count += 1
            elif g.result == 'Genuine':
                g_count +=1
            else:
                pass
        real_time_s[m] = {'Genuine': g_count, 'Counterfeit': c_count, 'Report': 0}

    for (minute, group) in g_report:
        min = minute
        r_count = 0
        for g in group:
            if g.type == 'Report':
                r_count += 1
            else:
                pass

        if r_count == 0:
            continue

        if min in real_time_s:
            real_time_s[min]['Report'] = r_count
        else:
            real_time_s[min] = {'Genuine': 0, 'Counterfeit': 0, 'Report': r_count}

    return jsonify({
        'status': real_time_s
    })



@api.route('/dashboard2/')
def real_time_static():
    start, end = static_date_range()
    statics = TsCertReportCount.query.filter(TsCertReportCount.registerDt.between(start, end)).order_by(TsCertReportCount.registerDt.desc()).all()
    g_statics = groupby(statics, lambda s: s.registerDt.strftime('%Y-%m-%d'))

    real_time_static = dict()
    for (minute, group) in g_statics:
        m = minute
        g_count = 0
        s_count = 0
        c_count = 0
        r_count = 0
        etc = 0
        for g in group:
            if g.type == 'Genuine':
                g_count += g.count
            elif g.type == 'Share':
                s_count += g.count
            elif g.type == 'Counterfeit':
                c_count += g.count
            elif g.type == 'Report':
                r_count += g.count
            else:
                etc += g.count
        total = g_count + c_count + etc
        real_time_static[m] = {'Total': total, 'Genuine': g_count, 'Share': s_count, 'Counterfeit': c_count, 'Report': r_count, 'ETC': etc}

    return jsonify({
        'status': real_time_static
    })