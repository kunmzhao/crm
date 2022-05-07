from django.urls import path, include
from django.conf.urls import url
from .views import role

urlpatterns = [
    url('^role/list/$', role.role_list, name='role_list'),
    url('^role/add/$', role.role_add, name='role_add'),
    url('^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),
    url('^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),

]
