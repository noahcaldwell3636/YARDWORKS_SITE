from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.render_landing_page, name="Landing_Page"),
]