from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Show,SType,Unit
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from django.views.generic import View
# Create your views here.

def index(requests):
    return HttpResponse("mmm")

def topApi(requests):
    article_list = Show.objects.filter(isShow=True, isTop=True).order_by('id')
    t = SType(name="未分类")
    for i in article_list:
        if not i.announce.s_type:
            i.announce.s_type = t
    res = {
        'codeDesc': 'success',
        'count': article_list.count(),
        'content': [{
                        'id': i.id,
                        'title': i.announce.title,
                        'content': i.announce.content,
                        'sType': i.announce.s_type.name,
                        'oriType': i.announce.ori_type,
                        'unit': i.announce.unit.name,
                        'click': i.click,
                        'approve': i.approve
                    } for i in article_list]
    }
    return HttpResponse(json.dumps(res), content_type="application/json")

def articleApi(requests):
    s = Show.objects.filter(isShow=True, isTop=False).order_by('id')
    p = Paginator(s, 30)
    try:
        page = int(requests.GET.get('page', 1))
        article_list = p.page(page)
    except(EmptyPage, InvalidPage):
        article_list = p.page(1)
    t = SType(name="未分类")
    for i in article_list:
        if not i.announce.s_type:
            i.announce.s_type = t
    res = {
        'codeDesc': 'success',
        'content': [{
                        'id': i.id,
                        'title': i.announce.title,
                        'content': i.announce.content,
                        'sType': i.announce.s_type.name,
                        'oriType': i.announce.ori_type,
                        'unit': i.announce.unit.name,
                        'click': i.click,
                        'approve': i.approve
                    } for i in article_list]
    }
    return HttpResponse(json.dumps(res), content_type="application/json")

def getTypeAndUnit(requests):
    st = SType.objects.all()
    count_dict = []
    for i in st:
        count_dict.append(i.name)
    cont = {
        'type': count_dict,
    }
    u = Unit.objects.all()
    count_dict = []
    for i in u:
        count_dict.append(i.name)
    cont['unit'] = count_dict
    res = {
        'codeDesc': 'success',
        'content': cont
    }
    return HttpResponse(json.dumps(res), content_type="application/json")

@csrf_exempt
def infoByType(requests):
    wt = requests.POST.getlist("type[]")
    unit = requests.POST.getlist("unit[]")
    s = Show.objects.filter(announce__s_type__name__in=wt, announce__unit__name__in=unit, isTop=False,
                            isShow=True).order_by('id')
    if(len(wt) == 0):
        s = Show.objects.filter(announce__unit__name__in=unit, isTop=False,
                                isShow=True).order_by('id')
    if(len(unit) == 0):
        s = Show.objects.filter(announce__s_type__name__in=wt, isTop=False,
                                isShow=True).order_by('id')
    if(len(wt) == 0 and len(unit) == 0):
        s = Show.objects.filter(isTop=False,
                                isShow=True).order_by('id')
    p = Paginator(s, 30)
    try:
        page = int(requests.POST.get('page', 1))
        article_list = p.page(page)
    except(EmptyPage, InvalidPage):
        article_list = p.page(1)
    t = SType(name="未分类")
    for i in article_list:
        if not i.announce.s_type:
            i.announce.s_type = t
    res = {
        'codeDesc': 'success',
        'content': [{
                        'id': i.id,
                        'title': i.announce.title,
                        'content': i.announce.content,
                        'sType': i.announce.s_type.name,
                        'oriType': i.announce.ori_type,
                        'unit': i.announce.unit.name,
                        'click': i.click,
                        'approve': i.approve
                    } for i in article_list]
    }
    return HttpResponse(json.dumps(res), content_type="application/json")

def clickandapprove(requests):
    t = requests.GET.get('ca', 'c')
    i = int(requests.GET.get('id', 1))
    s = Show.objects.get(id=i)
    if t == 'c':
        s.click = s.click + 1
    else:
        s.approve = s.approve + 1
    s.save()
    return HttpResponse("Success")