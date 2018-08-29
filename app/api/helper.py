from datetime import *
from dateutil.relativedelta import relativedelta
from flask import request, app, current_app
from datetime import datetime
from dateutil.relativedelta import *


def date_range():

    query_data = request.args
    start, end = query_data.get('start'), query_data.get('end')
    s_default = datetime.today() - relativedelta(months=3)
    e_default = datetime.today()

    start_date = datetime.strptime(start, '%Y-%m-%d').date() if start is not None else s_default
    end_date = datetime.strptime(end, '%Y-%m-%d').date() if end is not None else e_default

    return start_date, end_date


def log_date_range():

    query_data = request.args
    start, end = query_data.get('start'), query_data.get('end')

    today = datetime.now()
    loginit = datetime.now() - relativedelta(months=3)

    start_date = datetime.strptime(start, '%Y-%m-%d').date() if start is not None else today
    end_date = datetime.strptime(end, '%Y-%m-%d').date() if end is not None else loginit
    return start_date, end_date


def page_and_search():
    query_data = request.args
    page, search = query_data.get('page', 1), query_data.get('query', '')
    return page, search


def cert_date_range():

    end = datetime.now() - relativedelta(months=1)
    start = datetime.now() - relativedelta(hours=8, months=1)

    return start, end

def static_date_range():

    end = datetime.now()- relativedelta(months=1)
    start = datetime.now() - relativedelta(months=2)

    return start, end


def allowed_file(filename):

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'txt'])

    return '.' in filename and \
             filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def page_and_search():
    query_data = request.args
    page, search = query_data.get('page', 1), query_data.get('query', '')
    return page, search

def app_sql():
    frontsql = "select bstnt.th_certification.* , bstnt.td_device.model, bstnt.td_device.language, bstnt.td_device.dtRegistered ,bstnt.td_app.name_kr as appname, bstnt.td_black_list.blType, bstnt.td_black_list.delYN, bstnt.td_black_list.idx as idBlack\
          from bstnt.th_certification\
          left join bstnt.td_device \
          on bstnt.th_certification.deviceID = bstnt.td_device.pushToken \
          left join bstnt.td_app\
          on bstnt.td_device.appCode = bstnt.td_app.code \
          left join bstnt.td_black_list \
          on bstnt.th_certification.deviceID = bstnt.td_black_list.pushToken\
          where deviceID like '"
    countsql = "select count(*) from bstnt.th_certification left join bstnt.td_device on bstnt.th_certification.deviceID = bstnt.td_device.pushToken left join bstnt.td_app\
          on bstnt.td_device.appCode = bstnt.td_app.code left join bstnt.td_black_list on bstnt.th_certification.deviceID = bstnt.td_black_list.pushToken\
          where deviceID like '"


    return frontsql, countsql
