#coding=utf-8
from django.shortcuts import render
from userlogin.models import *
from django.http import JsonResponse
from cart.models import *
from goods.models import *
from userlogin import user_decoration
from django.shortcuts import redirect
# Create your views here.
@user_decoration.login
def Cart(request):
    client = user.objects.filter(id=request.session["user_id"])[0]
    notorder = CartInfo.objects.filter(username=client.id, isOrder=0)
    for g in notorder:
        g.isDelete = 0
        g.save()
    cartlist = []

    count = CartInfo.objects.filter(username=client.id,isOrder=0).count()
    product = CartInfo.objects.filter(username = client.id,isOrder=0).values("goods")
    total = CartInfo.objects.filter(username = client.id,isOrder=0).values("count")
    for c,num in zip(product,total):
        cartlist.append({"goods":GoodsInfo.objects.filter(id = c["goods"]),
                         "count":num})
    content = {
        "count":count,
        "product":cartlist,
    }
    return render(request,"cart.html",content)
#商品加入购物车的处理
@user_decoration.login
def add_cart(request, g_count, goods_id):
    cart = CartInfo()
    client = user.objects.filter(id = request.session["user_id"])[0]
    count = CartInfo.objects.filter(username = client.id,isOrder=0).count()
    count += 1
    cart.username_id = client.id
    cart.goods_id = goods_id
    cart.count = g_count
    cart.save()
    counts = count
    return JsonResponse({"count": counts})
@user_decoration.login
def del_cart(request,cart_id):
    id = request.session["user_id"]
    cart_id = CartInfo.objects.filter(username = id ,isOrder=0)[int(cart_id)]
    CartInfo.objects.filter(id = cart_id.id).delete()
    CartInfo.save()
@user_decoration.login
def add_count(request,goods_id,count):
    id = request.session["user_id"]
    cart_id = CartInfo.objects.filter(username = id ,isOrder=0)[int(goods_id)]
    CartInfo.objects.filter(id = cart_id.id).update(count =count)
    CartInfo.save()
@user_decoration.login
def minus_count(request,goods_id,count):
    id = request.session["user_id"]
    cart_id = CartInfo.objects.filter(username = id ,isOrder=0)[int(goods_id)]
    CartInfo.objects.filter(id=cart_id.id).update(count=count)
    CartInfo.save()


#判断复选框是否被选
@user_decoration.login
def existselect(request,flag,cart_id):
    user_id=request.session["user_id"]
    cart = CartInfo.objects.filter(username=user_id,isOrder=0)[int(cart_id)]
    if flag=="1":
        cart.isDelete = 1
    else:
        cart.isDelete = 0
    cart.save()
@user_decoration.login
def existorder(request,index):
    user_id = request.session["user_id"]

    if index=="deal":
        cart = CartInfo.objects.filter(username=user_id, isDelete=1)
        for c in cart:
            c.isOrder = 0
            c.isDelete = 0
            c.save()
            return redirect("/cart")
    else:
        cart = CartInfo.objects.filter(username=user_id, isDelete=1)[int(index)]
        cart.isOrder = 1
        cart.save()
        return redirect("/order")