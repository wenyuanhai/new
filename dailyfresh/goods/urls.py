from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'index$',views.index),
    url(r"detail/(\d+)/(\d+)$",views.detail),
    url(r"goods_list/(\d+)/(\d+)/(\d+)?$",views.goods_list)
]