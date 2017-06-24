#coding=utf-8
from django.shortcuts import render
from userlogin.models import user
from goods.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from cart.models import *
# Create your views here.
def index(request):
    count =0
    if request.session.has_key("user_id"):
        client = user.objects.filter(id = request.session['user_id'])[0]
        count = CartInfo.objects.filter(username=client.id).count()
    popular_fruit = GoodsInfo.objects.filter(gtype=1).order_by("-gclick")[:3]
    popular_seafoods = GoodsInfo.objects.filter(gtype=2).order_by("-gclick")[:3]
    fruitlist = GoodsInfo.objects.filter(gtype=1)[:4]
    seafoods = GoodsInfo.objects.filter(gtype=2)[:4]
    for f in seafoods:
        print f.gpic
    content = {
        # "user_name":name,
        # "error_name":0,
        "popular_fruit":popular_fruit,
        "fruitlist":fruitlist,
        "popular_seafoods":popular_seafoods,
        "seafoods":seafoods,
        "count":count
    }
    return render(request,"index.html",content)
#商品详情页的处理
def detail(request,gtype_id,food_id):
    count = 0
    if request.session.has_key("user_id"):
        client = user.objects.filter(id = request.session['user_id'])[0]
        count = CartInfo.objects.filter(username=client.id).count()
    popular_foods = GoodsInfo.objects.filter(gtype=gtype_id).order_by("-gclick")[:2]
    product = GoodsInfo.objects.filter(id=food_id)[0]
    product.gclick+=1
    product.save()
    content = {
        "product":product,
        "popular_foods":popular_foods,
        "error_name":0,
        "count":count
    }
    re = render(request,"detail.html",content)
    # re.set_cookie("goods_id",food_id)
    #设置cookie记录浏览历史
    history_id = request.COOKIES.get("goods_id","")
    history_idlist = "%s"%history_id
    print history_idlist
    id_list =  history_idlist.split(",")

    if len(id_list) != 0:
        if id_list.count(food_id)>=1:
            id_list.remove(food_id)
        id_list.insert(0,food_id)
        if len(id_list)>=6:
            del id_list[5]
        id_list = ",".join(id_list)
        re.set_cookie("goods_id", id_list)
        return re
    else:
        re.set_cookie("goods_id", food_id)
        return re
#显示商品列表页
def goods_list(request,gtype_id,pagenum,sort):
    goodslist = GoodsInfo.objects.filter(gtype=gtype_id)
    if sort=="1":
        goodslist = GoodsInfo.objects.filter(gtype=gtype_id).order_by("-gprice")
    elif sort=="2":
        goodslist = GoodsInfo.objects.filter(gtype=gtype_id).order_by("-gclick")
    client = user.objects.filter(id = request.session["user_id"])[0]
    popular_goods = GoodsInfo.objects.filter(gtype = gtype_id).order_by("-gclick")[:2]
    count = CartInfo.objects.filter(username=client.id).count()
    #分页信息
    pagi = Paginator(goodslist,10)
    page = pagi.page(pagenum)
    content = {
        "popular_goods":popular_goods,
        "pagi":pagi,
        "page":page,
        "gtype_id":gtype_id,
        "sort":sort,
        "count":count
    }
    return render(request,"list.html",content)
