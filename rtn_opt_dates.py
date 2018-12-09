# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


def rtn_dates(beg, end=None, using_weekend=False, rtn_string=True):
    """
    :param beg: Date String, e.g. 20170901, 2017-09-01
    :param end: Date String, e.g. 20170901, 2017-09-01, if not specified, using current date
    :param using_weekend:
    :param rtn_string: (indicate whether the returned value is a string or a python date object
    :return:

    Example:
        rtn_dates('20170801', '20170805', using_weekend=True, rtn_string=True)
        =['20170801', '20170802', '20170803', '20170804', '20170805']
    """
    beg = beg.replace("-", "")
    beg_date = datetime.strptime(beg, "%Y%m%d").date()

    if isinstance(end, str) and len(end):
        end = end.replace("-", "")
        end_date = datetime.strptime(end, "%Y%m%d").date()
    else:
        end_date = datetime.now().date()
    test_dates = []
    while beg_date <= end_date:
        week_day = beg_date.weekday() + 1  # .weekday() : Monday: 0, Sunday: 6
        if (week_day != 6 and week_day != 7) or using_weekend:
            test_dates.append(beg_date)
        beg_date += timedelta(days=1)
    if rtn_string:
        test_dates = list(map(lambda x: x.strftime("%Y%m%d"), test_dates))
    return test_dates


def _rtn_opt_dates(d, using_weekend=False, rtn_string=True):
    """
    :param d: date string: e.g. 20170901-20170920,20171001,20171020
    :param using_weekend:
    :param rtn_string:
    :return:
    """
    test_dates = []
    ds = d.replace(' ', '').split(',')
    for dd in ds:
        if '-' in dd:
            ddd = dd.split('-')
            test_dates += rtn_dates(ddd[0], ddd[1], using_weekend, False)
            pass
        else:
            ddd = datetime.strptime(dd, "%Y%m%d").date()
            week_day = ddd.weekday() + 1
            if (week_day != 6 and week_day != 7) or using_weekend:
                test_dates.append(ddd)
    if rtn_string:
        test_dates = list(map(lambda x: x.strftime("%Y%m%d"), test_dates))
    return test_dates


def rtn_opt_dates(d, using_weekend=False, rtn_string=True):
    """
    with exclusive feature
    :param d: date string: e.g. 20170901-20170920,20171001,20171020\20170905
    :param using_weekend:
    :param rtn_string:
    :return:
    """
    if '\\' in d:
        dd = d.split('\\')
        dd1 = _rtn_opt_dates(dd[0], using_weekend, rtn_string)
        dd2 = _rtn_opt_dates(dd[1], using_weekend, rtn_string)
        return sorted(list(set(dd1) - set(dd2)))
    else:
        return _rtn_opt_dates(d, using_weekend, rtn_string)

if __name__ == "__main__":
    print(rtn_opt_dates('20170521-20170531,20170603-20170701, 20170716'))

    print(rtn_opt_dates('20170521-20170531,20170603-20170701, 20170716\\20170613'))

    print(rtn_dates('20170521', '20170621'))        