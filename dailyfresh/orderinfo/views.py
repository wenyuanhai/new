#coding=utf-8
from django.shortcuts import render
from userlogin import user_decoration
from userlogin.models import *
from goods.models import *
from django.db.models import Q
from cart.models import *
import json
import time
from orderinfo.models import *
from django.shortcuts import redirect
from decimal import *
from django.db import transaction

# Create your views here.

@user_decoration.login
def order(request):
    list = []
    client = user.objects.filter(id = request.session["user_id"])[0]
    goods= GoodsInfo.objects.filter(cartinfo__isDelete=1,cartinfo__isOrder=1,cartinfo__username=client.id)
    count = CartInfo.objects.filter(isOrder=1,isDelete=1,username=client.id)
    for g in count:
        list.append(g.count)
    content={
        "address":client.ushou,
        "goods":goods,
        "list":json.dumps(list)
    }
    return render(request,"place_order.html",content)

@user_decoration.login
@transaction.atomic()
def place_order(request,tp):
    client = user.objects.filter(id=request.session["user_id"])[0]
    goods = GoodsInfo.objects.filter(Q(cartinfo__isDelete=1)
                                     &Q(cartinfo__isOrder=1)
                                     &Q(cartinfo__username=client.id))
    cartlist = CartInfo.objects.filter(isDelete=1,isOrder=1, username=client.id)
    nowtime = int(time.time())
    savepoint = transaction.savepoint()
    if tp>0:
        try:
            for good,cart in zip(goods,cartlist):
                order = OrderInfo()
                print "开始保存"
                order.ouserid_id = client.id
                order.orderid = nowtime
                order.ogid_id = good.id
                order.ocartid_id = cart.id
                order.ogprice = good.gprice
                order.ototal = cart.count*good.gprice
                order.paystatic = 1
                order.save()
                cart.isDelete = 0
                cart.save()
                print "end"
        except:
            transaction.savepoint_rollback(savepoint)
            return redirect("/cart")
    return redirect("/user/user_order/1")

#定时执行的代码
# import datetime
# from apscheduler.scheduler import Scheduler
# sched = Scheduler()
# @sched.interval_schedule(seconds=3600)
# def mytask():
#     print 6666666
#     cartlist = []
#     orderlist = []
#     print CartInfo.objects.values("id")
#     print OrderInfo.objects.values("ocartid")
#     for c in CartInfo.objects.values("id"):
#         print c.id
#
# sched.start()
