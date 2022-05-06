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
                                                                                  'permissions__url').distinct()
    # 获取权限中的所有URL
    permission_list = [item['permissions__url'] for item in permission_queryset]

    # 将权限信息写入session中
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
