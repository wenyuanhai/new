from django.db import models

# Create your models here.
class user(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uadd = models.CharField(max_length=100,default="")
    ushou = models.CharField(max_length=60,default="")
    uyoubian = models.CharField(max_length=10,default="")
    uphonenum = models.CharField(max_length=11,default="")
    uemail = models.CharField(max_length=15)
