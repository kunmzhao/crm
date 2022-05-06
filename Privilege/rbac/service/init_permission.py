from django.conf import settings


def init_permission(user_obj, request):
    """
    用户权限的初始化
    :param user_obj: 当前登陆用户
    :param request: 请求
    :return:
    """

    # 本次查询垮了两张表，注意去重和为空的筛选
    permission_queryset = user_obj.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                  'permissions__title',
                                                                                  'permissions__url',
                                                                                  'permissions__is_menu',
                                                                                  'permissions__icon').distinct()
    # 获取权限中的所有URL+菜单信
    menu_list = []
    permission_list = []
    for item in permission_queryset:
        permission_list.append(item['permissions__url'])
        # 可以成为菜单
        if item.get('permissions__is_menu'):
            temp = {
                'title': item['permissions__title'],
                'icon': item['permissions__icon'],
                'url': item['permissions__url']
            }
            menu_list.append(temp)
    # 将权限信息写入session中
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # 将菜单信息写入session中
    request.session[settings.MENU_SESSION_KEY] = menu_list
