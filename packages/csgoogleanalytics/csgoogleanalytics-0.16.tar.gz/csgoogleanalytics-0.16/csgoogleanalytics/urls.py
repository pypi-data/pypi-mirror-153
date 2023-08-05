from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^set_google$', views.set_google, name="set_google"),
    url(r'^auth_return$', views.auth_return, name="auth_return"),
    url(r'^select_property$', views.select_property, name="select_property"),
    url(r'^set_property/(?P<track_id>[0-9]+)$', views.set_property, name="set_property"),
]
