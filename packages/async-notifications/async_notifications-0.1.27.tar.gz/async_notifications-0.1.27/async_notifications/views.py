from django.http import JsonResponse
from django.http.request import QueryDict
from async_notifications.models import NewsLetterTemplate
from async_notifications.utils import get_newsletter_context, get_basemodel_info, get_model
from django.db.models.query_utils import Q
from .settings import (NOTIFICATION_GROUP_MODEL,
                       NOTIFICATION_USER_MODEL,
                       USER_LOOKUP_FIELDS,
                       GROUP_LOOKUP_FIELDS)

Group = get_model(NOTIFICATION_GROUP_MODEL)
User = get_model(NOTIFICATION_USER_MODEL)


def updatenewscontext(request, pk):
    dev = []
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        for i in get_newsletter_context(obj.model_base):
            dev.append(
                {
                    'id': i[0],
                    'text': i[0] + " -- " + i[1]
                }
            )

    return JsonResponse({'results': dev, "pagination": {"more": False}})


def get_form_data(request):
    dev = None
    try:
        dev = QueryDict(request.POST.get('recipient'))
    except:
        dev = None

    return dev


def fromnewscontext(request, pk):
    dev = ""
    media = ""
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        inst = get_basemodel_info(obj.model_base)
        if inst:
            klass = inst[2]()
            f = klass.get_form(get_form_data(request))
            dev = str(f)
            media = str(f.media)
    return JsonResponse({'form': dev, 'media': media})


def preview_email_newsletters(request, pk):
    dev = []
    obj = NewsLetterTemplate.objects.filter(pk=pk).first()
    if obj:
        inst = get_basemodel_info(obj.model_base)
        if inst:
            klass = inst[2]()
            form = klass.get_form(get_form_data(request))
            klass.set_form(form)
            klass.get_queryset()
            dev = klass.get_emails()
    return JsonResponse({'emails': dev})

def get_filters(filters, q):
    fields = None
    for f in filters['filter']:
        if fields is None:
            fields = Q(**{f: q})
        else:
            fields |= Q(**{f: q})
    return fields

def get_display(obj, name):
    if "__" in name and name != '__str__':
        names = name.split("__")
        objs = getattr(obj, names[0])
        return get_display(objs, "__".join(names[1:]))
    nname = getattr(obj, name)
    if callable(nname):
        nname = nname()
    return nname


def get_query_groups( q, request):
    fields = get_filters(GROUP_LOOKUP_FIELDS, q)
    groups = Group.objects.filter(fields)
    gs = []
    for g in groups:
        name = get_display(g, GROUP_LOOKUP_FIELDS['display'])
        gs.append({'value': "%s@group" % name.replace(" ", "__"), 'name': name})
    return gs


def get_user_emails(filters):
    users = User.objects.filter(filters).order_by(USER_LOOKUP_FIELDS['order_by'])
    usermails = []
    for user in users:
        name = get_display(user, USER_LOOKUP_FIELDS['display'])
        usermails.append({'value':  get_display(user, USER_LOOKUP_FIELDS['email']),
                          'code': name})
    return usermails

def search_email(request):
    value = request.GET.get('values', '')
    filters = get_filters(USER_LOOKUP_FIELDS, value)
    emails=get_user_emails(filters)
    emailg = get_query_groups(value, request)
    return JsonResponse(emails+emailg, safe=False)