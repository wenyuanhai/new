from django.db import models
from userlogin.models import *

# Create your models here.
class OrderInfo(models.Model):
    orderid = models.IntegerField()
    ouserid = models.ForeignKey("userlogin.user")
    ogid = models.ForeignKey("goods.GoodsInfo")
    ocartid = models.ForeignKey("cart.CartInfo")
    ogprice = models.DecimalField(max_digits=6,decimal_places=2)
    ototal = models.DecimalField(max_digits=6,decimal_places=2)
    paystatic = models.BooleanField(default=0)



