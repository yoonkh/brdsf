from datetime import *
from dateutil.relativedelta import relativedelta
from flask import request
# from itertools import groupby


def log_date_range():

    query_data = request.args
    start, end = query_data.get('start'), query_data.get('end')

    today = datetime.now()
    loginit = datetime.now() - relativedelta(months=3)

    start_date = datetime.strptime(start, '%Y-%m-%d').date() if start is not None else today
    end_date = datetime.strptime(end, '%Y-%m-%d').date() if end is not None else loginit
    return start_date, end_date


# def date_range_by_year():
#
#     year = request.args.get('year')
#     this_year = datetime.now().year
#     oneday = timedelta(1)
#
#     if year is not None:
#         start_date = datetime.strptime(year, '%Y').date()
#         end_date = datetime.strptime(str(int(year)+1), '%Y').date() - oneday
#     else:
#         start_date = datetime.strptime(str(this_year), '%Y').date()
#         end_date = datetime.strptime(str(this_year+1), '%Y').date() - oneday
#
#     return start_date, end_date
#
#
# def group_by_month(worktimes):
#
#     initial_worktimes = {'work': 0, 'over_work': 0}
#     monthes = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
#                7: 'jul', 8: 'aug', 9: 'sept', 10: 'oct', 11: 'nov', 12: 'dec'}
#
#     monthly_worktimes = dict()
#     for month_num in monthes:
#         month = monthes[month_num]
#         monthly_worktimes[month] = initial_worktimes.copy()
#
#     for worktime in worktimes:
#         month_num = worktime.work_date.month
#         month = monthes[month_num]
#
#         month_worktimes = monthly_worktimes[month]
#         month_worktimes['work'] += worktime.work
#         month_worktimes['over_work'] += worktime.over_work
#
#     # mws = groupby(worktimes, lambda w: w.work_date.month)
#     # for (month, worktimes) in mws:
#     #     ws = sum(w.work for w in worktimes)
#     #     ows = sum(w.over_work for w in worktimes)
#     #
#     #     monthly_worktimes[monthes[month]]['work'] = ws
#     #     monthly_worktimes[monthes[month]]['over_work'] = ows
#
#     return monthly_worktimes
