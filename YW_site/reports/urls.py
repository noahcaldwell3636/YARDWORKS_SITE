from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.render_report, name="index"),
    url(r'^sales/', views.render_report, name='sales_report')
]