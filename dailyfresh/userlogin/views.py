#coding=utf-8
from django.shortcuts import render
from userlogin.models import user
from hashlib import sha1
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import chardet
from goods.models import *
from . import user_decoration
from orderinfo.models import *
from django.db.models import Count
from decimal import *
from django.db.models import Sum
from django.core.paginator import Paginator
# Create your views here.
def login(request):
    uname = request.COOKIES.get("user_name","")
    content = {
        "user_name":uname,
        "error":0,
    }
    return render(request,"login.html",content)
def logout(request):
    request.session.flush()
    return redirect("/user/login")
def register(request):
    return render(request,"register.html")
#注册
def register_handler(request):
    #接受数据
    req = request.POST
    uname = req.get("user_name")
    pwd = req.get("pwd")
    cpwd = req.get("cpwd")
    email = req.get("email")
    #比较两次密码是否相同
    if pwd!= cpwd or uname == "":
        return redirect("/user/register")
    #密码加密
    s1 = sha1()
    s1.update(pwd)
    pwd2 = s1.hexdigest()

    #保存用户数据到数据库
    client = user()
    client.uname = uname
    client.upwd = pwd2
    client.uemail = email
    client.save()
    return redirect("/user/login")
#注册判断用户名是否存在
def register_exist(request):
    #参数在url中进行传递的用request.GET.get（）
    name = request.GET.get("uname")
    count = user.objects.filter(uname = name).count()
    return JsonResponse({"count":count})

#登录处理
def login_handler(request):
    # 参数通过表单传递的用request.POST.get（）
    name = request.POST.get("username")
    upwd = request.POST.get("pwd")
    jizhu = request.POST.get("jizhu")
    client = user.objects.filter(uname=name)
    url = request.COOKIES.get("url", "/goods/index")
    if len(client):

        s1= sha1()
        s1.update(upwd)
        pwd2 = s1.hexdigest()
        if client[0].upwd==pwd2:
            red = HttpResponseRedirect(url)
            if jizhu != 0:
                red.set_cookie("user_name",name)
            else:
                red.set_cookie("user_name","",max_age=-1)
            # request.session['user_name'] = name
            request.session['user_id'] = client[0].id
            request.session["username"] = client[0].uname
            request.session.set_expiry(0)
            return red
    else:
        content = {
            "user_name":name,
            "error":1
        }
        return render(request,'login.html',content)
#用户中心页
@user_decoration.login
def user_info(request):
    history_list = []
    client = user.objects.filter(id=request.session['user_id'])[0]
    goods_id = request.COOKIES.get("goods_id","")
    string = "%s"%goods_id
    id_list = string.split(",")
    try:
        for g_id in id_list:
            history_list.append(GoodsInfo.objects.filter(id = g_id))
    except:
        pass
    content={
        "error_name":0,
        'email':client.uemail,
        'user_name':client.uname,
        "history_list":history_list
    }
    print history_list
    return render(request,"user_center_info.html",content)
#收货地址处理页
@user_decoration.login
def user_site(request):
    client = user.objects.filter(id=request.session['user_id'])[0]
    receiver_add = ""
    receiver = ""
    address = ""
    phone = ""
    zipcode = ""
    # 查看client是否有收件人地址
    if client.ushou!="":
        receiver_add = client.ushou
        receiver = receiver_add.split(" ")[0]
        address = receiver_add.split(" ")[1]
        phone = receiver_add.split(" ")[2]
        zipcode = receiver_add.split(" ")[3]
    if request.method=="POST":
        receiver = request.POST.get("receiver")
        print type(receiver)
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        zipcode = request.POST.get("zipcode")
        receiver_add = (
            str(address.encode("utf8"))+" "+\
            str(zipcode.encode("utf8"))+" "+\
            str(receiver.encode("utf8"))+" "+\
            str(phone.encode("utf8"))
        )
        print type(receiver_add)

        #保存收件人地址到数据库
        client.ushou = receiver_add
        client.save()
    content = {
        "error_name": 0,
        'user_name': client.uname,
        "receiver_add": receiver_add,
        "address":address,
        "zipcode":zipcode,
        "receiver":receiver,
        "phone":phone
    }
    return render(request,'user_center_site.html',content)
#订单页
@user_decoration.login
def user_order(request,index):
    num = Decimal(0)
    if index=="":
        pagenum = 1
    else:
        pagenum=int(index)
    client = user.objects.filter(id=request.session['user_id'])[0]
    orderlist = OrderInfo.objects.filter(ouserid=client.id)
    heji = orderlist.values("orderid").annotate(Sum("ototal"))
    p = Paginator(heji, 2)
    pageindex = p.page_range
    page = p.page(pagenum)
    print page.object_list
    content = {
        "orderlist": orderlist,
        "heji":heji,
        "pageindex":pageindex,
        "page":page
    }
    return render(request,"user_center_order.html",content)

