from django.db import models

# Create your models here.
class CartInfo(models.Model):
    username = models.ForeignKey("userlogin.user")
    goods = models.ForeignKey("goods.GoodsInfo")
    count = models.IntegerField()
    isDelete = models.BooleanField(default=0)
    isOrder = models.BooleanField(default=0)
