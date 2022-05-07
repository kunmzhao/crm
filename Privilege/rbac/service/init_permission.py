from django.conf import settings


def init_permission(user_obj, request):
    """
    用户权限的初始化
    :param user_obj: 当前登陆用户
    :param request: 请求
    :return:
    """

    # 本次查询垮了三张表，注意去重和为空的筛选
    permission_queryset = user_obj.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                  'permissions__title',
                                                                                  'permissions__url',
                                                                                  'permissions__pid__id',
                                                                                  'permissions__pid__title',
                                                                                  'permissions__pid__url',
                                                                                  'permissions__is_menu',
                                                                                  'permissions__icon',
                                                                                  'permissions__menu__id',
                                                                                  'permissions__menu__icon',
                                                                                  'permissions__menu__title',
                                                                                  ).distinct()
    # 获取权限中的所有URL+菜单信
    menu_dict = {}
    permission_list = []
    for item in permission_queryset:
        permission_list.append(
            {
                'id': item['permissions__id'],
                'url': item['permissions__url'],
                'pid': item['permissions__pid__id'],
                'title': item['permissions__title'],
                'p_title': item['permissions__pid__title'],
                'p_url': item['permissions__pid__url'],
            }
        )
        menu_id = item['permissions__menu__id']
        if not menu_id:
            continue
        node = {
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'icon': item['permissions__icon'],
            'id': item['permissions__id']
        }
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node],
            }
    print(menu_dict)
    # 将权限信息写入session中
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    # 将菜单信息写入session中
    request.session[settings.MENU_SESSION_KEY] = menu_dict
