from datetime import *
from dateutil.relativedelta import relativedelta


def cert_date_range():

    end = datetime.now() - relativedelta(days=9)
    start = datetime.now() - relativedelta(hours=8, days=9)

    return start, end

def static_date_range():

    end = datetime.now()
    start = datetime.now() - relativedelta(days=10, months=1)

    return start, end