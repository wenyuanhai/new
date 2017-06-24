from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class TypeInfo(models.Model):
    ctitle = models.CharField(max_length=20)
    cisdelete = models.BooleanField(default=0)
    def __str__(self):
        return self.ctitle.encode("utf-8")

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='static/images/goods_img')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    gisdelete = models.BooleanField(default=0)
    gunit = models.CharField(max_length=20,default='500g')
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo)
    def __str__(self):
        return self.gtitle.encode("utf-8")
