from django.conf.urls import include, url
from app_library import views

urlpatterns = [
    # url(r'^$', views.render_table, name="library"),
    url(r'^ByLocation/', views.render_table_byloc, name="byloc"),
    url(r'^ByID/', views.render_table_byid, name="byid"),
    url(r'^ByMake/', views.render_table_bymake, name="bymake"),
    url(r'^equipment/', views.render_indiv_eq, name="eq_view"),
    url(r'^sheets/', views.render_eq_sheet_table, name="eq_sheet_view"),
    url(r'^sheet_submission/', views.render_sheet_submission, name="sheet_submission"),
]