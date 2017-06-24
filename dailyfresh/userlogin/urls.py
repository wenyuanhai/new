from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"login$",views.login),
    url(r"login_handler$",views.login_handler),
    url(r"register$",views.register),
    url(r"register_handler$",views.register_handler),
    url(r"register_exist/$",views.register_exist),
    url(r'user_info$',views.user_info),
    url(r'user_order/(.*)?$',views.user_order),
    url(r'user_site$',views.user_site),
    url(r"logout$",views.logout)

]