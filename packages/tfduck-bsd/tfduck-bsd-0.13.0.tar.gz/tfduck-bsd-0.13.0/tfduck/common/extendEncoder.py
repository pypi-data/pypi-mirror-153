# coding=utf-8
"""
@author: yx
@des: 可以转含有datetime和Decimal的json的方法
@用法: 
      from django.utils import simplejson
      from common.extendEncoder import DatetimeJSONEncoder
      j = {'a':45, 'b':78, 'now':datetime.datetime.now(), 'decimal':decimal.Decimal("100.254")}
      print simplejson.dumps(j, cls=DatetimeJSONEncoder)
      >>> {"a": 45, "now": "2011-03-25 17:59:43", "b": 78, "decimal": "100.254"}
"""

import datetime
import decimal
import json
import django
from django.utils.translation import ugettext_lazy


def safe_new_datetime(d):
    kw = [d.year, d.month, d.day]
    if isinstance(d, datetime.datetime):
        kw.extend([d.hour, d.minute, d.second, d.microsecond, d.tzinfo])
    return datetime.datetime(*kw)


def safe_new_date(d):
    return datetime.date(d.year, d.month, d.day)


class DatetimeJSONEncoder(json.JSONEncoder):
    """可以序列化时间的JSON"""

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        if isinstance(o, datetime.datetime):
            d = safe_new_datetime(o)
            return d.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))
        elif isinstance(o, datetime.date):
            d = safe_new_date(o)
            return d.strftime(self.DATE_FORMAT)
        elif isinstance(o, datetime.time):
            return o.strftime(self.TIME_FORMAT)
        elif hasattr(o, "_proxy____args"):
            return str(o)
        else:
            return super(DatetimeJSONEncoder, self).default(o)
