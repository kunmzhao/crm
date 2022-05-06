from django.shortcuts import HttpResponse, render, redirect
# TBD: 不要跨项目引入
from rbac.models import User
from rbac.service.init_permission import init_permission


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

    # 登陆成功，权限初始化
    init_permission(user_obj=user_obj, request=request)
    return redirect('/customer/list/')
