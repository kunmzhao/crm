from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import URLPattern, URLResolver
import re


def check_url_exclude(url):
    """
    排除特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归获取URL
    :param pre_namespace:namespace前缀，拼接name
    :param pre_url:url的前缀
    :param urlpatterns:路由关系列表
    :param url_ordered_dict:用于保存递归中获取的URL
    :return:
    """
    for item in urlpatterns:
        # 非路由分发
        if isinstance(item, URLPattern):
            # 没有别名name
            if not item.name:
                continue
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            # 拼接URL
            url = pre_url + item.pattern.regex.pattern
            url = url.replace('^', '').replace('$', '')  # 去掉终止符和起始符
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}
        # 路由分发，递归操作
        elif isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_ordered_dict)
        else:
            continue


def get_all_url_dict():
    """
    获取项目中的所有URL（必须有name别名）
    :return:
    """
    url_ordered_dict = OrderedDict()
    # 以字符串的形式导入模块
    md = import_string(settings.ROOT_URLCONF)
    # 递归获取所有的路由
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)
    return url_ordered_dict
