import re
from django.template import Library
from collections import OrderedDict
from django.conf import settings
from django.urls import reverse
from django.http import QueryDict
from rbac.service import urls

register = Library()


# @register.inclusion_tag('rbac/static_menu.html')
# def static_menu(request):
#     """
#     创建一级菜单
#     :return:
#     """
#     current_url = request.path_info
#     menu_list = request.session.get(settings.MENU_SESSION_KEY)
#     return {'menu_list': menu_list, 'current_url': current_url}

@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    创建二级菜单
    :return:
    """
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    # 将无序的字典转换为有序的
    key_list = sorted(menu_dict)
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        for per in val['children']:
            if per['id'] == request.current_selected_permission:
                val['class'] = ''
                per['class'] = 'active'
        ordered_dict[key] = val
    # 格式如下
    """
    {
        1: {
            'title': '信息管理',
            'icon': 'fa fa-audio-description',
            'children': [
                {
                    'title': '客户列表',
                    'url': '/customer/list/', 'icon': 'fa fa-address-book-o'
                }
            ]
        },
        2: {
            'title': '用户管理',
            'icon': 'fa fa-car',
            'children': [
                {
                    'title': '账单列表',
                    'url': '/payment/list/',
                    'icon': 'fa fa-id-card'
                }
            ]
        }
    }
    """

    return {'ordered_dict': ordered_dict}


@register.inclusion_tag('rbac/url_record.html')
def url_record(request):
    return {'url_record': request.url_record}


@register.filter
def has_permission(request, name):
    """
    判断是否有权限
    :param request:
    :param name:
    :return:
    """
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原有搜索条件的URL，替代模板中的
    :param request:
    :param name:
    :return:
    """
    return urls.memory_url(request, name, *args, **kwargs)
