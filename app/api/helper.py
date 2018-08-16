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