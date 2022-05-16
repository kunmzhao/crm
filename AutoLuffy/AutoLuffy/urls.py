"""AutoLuffy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from app01.views import user, host, account

urlpatterns = [
    url('admin/', admin.site.urls),

    url('login/', account.login, name='login'),
    url('logout/', account.logout, name='logout'),
    url('index/', account.index, name='index'),

    url('user/list/', user.user_list, name='user_list'),
    url('user/add/', user.user_add, name='user_add'),
    url('^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    url('^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    url('^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),

    url('host/list/', host.host_list, name='host_list'),
    url('host/add/', host.host_add, name='host_add'),
    url('^host/edit/(?P<pk>\d+)/$', host.host_edit, name='host_edit'),
    url('^host/del/(?P<pk>\d+)/$', host.host_del, name='host_del'),

    url('rbac/', include(('rbac.urls', 'rbac'), namespace='rbac')),
]
