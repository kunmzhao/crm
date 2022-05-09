from django.conf.urls import url
from .views import role, user, menu

urlpatterns = [
    url('^role/list/$', role.role_list, name='role_list'),
    url('^role/add/$', role.role_add, name='role_add'),
    url('^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),
    url('^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),

    url('^user/list/$', user.user_list, name='user_list'),
    url('^user/add/$', user.user_add, name='user_add'),
    url('^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    url('^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    url('^user/password/reset/(?P<pk>\d+)/$', user.user_password_reset, name='user_password_reset'),

    url('^menu/list/$', menu.menu_list, name='menu_list'),
    url('^menu/add/$', menu.menu_add, name='menu_add'),
    url('^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    url('^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='menu_del'),

    url('^second_menu/add/(?P<menu_id>\d+)$', menu.second_menu_add, name='second_menu_add'),
    url('^second_menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    url('^second_menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),

]
