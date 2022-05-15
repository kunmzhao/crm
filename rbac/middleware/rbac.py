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
        url_record = [
            {'url': '#', 'title': '首页'}
        ]
        # 判断是否需要登陆但无需权限的URL
        for item in settings.NO_PERMISSION_LIST:
            item = "^%s$" % item
            if re.match(item, current_url):
                request.current_selected_permission = 0
                request.url_record = url_record
                return None

        # 获取当前用户session中的权限
        permission_dict = request.session[settings.PERMISSION_SESSION_KEY]
        if not permission_dict:
            return HttpResponse('为获取用户权限信息，请登录')

        # 判断用户当前请求是否在session中
        flag = False
        for item in permission_dict.values():
            # 匹配应该严格
            reg = "^%s$" % (item['url'],)
            # 用户拥有权限
            if re.match(reg, current_url):
                flag = True
                # 菜单选中
                request.current_selected_permission = item['pid'] or item['id']
                # 导航条
                if not item['pid']:
                    url_record.append(
                        {'url': item['url'], 'title': item['title']}
                    )
                else:
                    url_record.extend([
                        {'url': item['p_url'], 'title': item['p_title']},
                        {'url': item['url'], 'title': item['title']}
                    ])
                request.url_record = url_record
                break

        if not flag:
            return HttpResponse('无权访问')
