import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        验证用户权限
        :param request:
        :return:
        """
        # 获取当前请求的url
        current_url = request.path_info

        # 判断url是否在白名单里面
        for item in settings.VALID_URL_LIST:
            item = "^%s$" % item
            if re.match(item, current_url):
                return None

        # 获取当前用户session中的权限
        permission_list = request.session[settings.PERMISSION_SESSION_KEY]
        if not permission_list:
            return HttpResponse('为获取用户权限信息，请登录')

        print(permission_list)
        # 判断用户当前请求是否在session中
        flag = False
        for item in permission_list:
            # 匹配应该严格
            reg = "^%s$" % (item['url'],)
            # 用户拥有权限
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                break

        if not flag:
            return HttpResponse('无权访问')
