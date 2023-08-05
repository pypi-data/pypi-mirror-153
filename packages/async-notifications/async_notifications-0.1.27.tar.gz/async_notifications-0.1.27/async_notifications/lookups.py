# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from django.db.models.query_utils import Q

from .settings import (NOTIFICATION_GROUP_MODEL,
                       NOTIFICATION_USER_MODEL)
from .utils import hexify, get_model

Group = get_model(NOTIFICATION_GROUP_MODEL)
User = get_model(NOTIFICATION_USER_MODEL)


class Person(object):
    email = None
    name = None

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.pk = hexify(email)

    def __str__(self):
        return "%s (%s)" % (self.name, self.email)


def get_filters(filters, q):
    fields = None
    for f in filters['filter']:
        if fields is None:
            fields = Q(**{f: q})
        else:
            fields |= Q(**{f: q})
    return fields


def get_display(obj, name):
    if "__" in name:
        names = name.split("__")
        objs = getattr(obj, names[0])
        return get_display(objs, "__".join(names[1:]))
    nname = getattr(obj, name)
    if callable(nname):
        nname = nname()
    return nname
