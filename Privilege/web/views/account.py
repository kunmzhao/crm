from django.shortcuts import HttpResponse, render, redirect
# TBD: 不要跨项目引入
from rbac.models import User


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 查找用户
    user_obj = User.objects.filter(name=username, password=password).first()
    # 用户名或者密码不正确
    if not user_obj:
        return render(request, 'login.html', {"info": '用户名或者密码不正确'})
    # 登陆成功，查找该用户的所有权限
    """
    本次查询垮了两张表，注意去重和为空的筛选
    """
    permission_queryset = user_obj.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                  'permissions__url').distinct()
    # 获取权限中的所有URL
    permission_list = [item['permissions__url'] for item in permission_queryset]

    # 将权限信息写入session中
    request.session['luffy_permission_url_list'] = permission_list
    return redirect('/customer/list/')
