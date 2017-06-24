from django.conf.urls import url
import views
urlpatterns = [
    url(r"^/$",views.order),
    url(r"place_order/(.+)$",views.place_order)
]