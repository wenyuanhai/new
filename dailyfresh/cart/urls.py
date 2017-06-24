from django.conf.urls import url
import views
urlpatterns = [
    url(r"^/$", views.Cart),
    url(r"add_cart/(\d+)/(\d+)$",views.add_cart),
    url(r"del_cart/(\d+)$",views.del_cart),
    url(r"add_count/(\d+)/(\d+)$",views.add_count),
    url(r"minus_count/(\d+)/(\d+)$",views.minus_count),
    url(r"existselect/(\d+)/(\d+)$",views.existselect),
    url(r"existorder/(.*)",views.existorder)
]