from django.urls import reverse
from django.http import QueryDict


def memory_reverse(request, name, *args, **kwargs):
    """
    反向生成url
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = "%s?%s" % (url, origin_params)
    return url


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原有搜索条件的URL
    :param request:
    :param name:
    :return:
    """
    base_url = reverse(name, args=args, kwargs=kwargs)
    # 当前url中无参数
    if not request.GET:
        return base_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return "%s?%s" % (base_url, query_dict.urlencode())
