from django.shortcuts import render, redirect
from app01.models import User
from rbac.service.init_permission import init_permission


def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'login.html')
    user = request.POST.get('username')
    pwd = request.POST.get('password')
    user_obj = User.objects.filter(name=user, password=pwd).first()
    print(user, pwd)
    if not user_obj:
        return render(request, 'login.html', {'info':'用户名或者密码不正确'})
    # 用户权限信息初始化
    init_permission(user_obj, request)
    return redirect('/index/')


def logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    request.session.delete()
    return redirect('/login/')


def index(request):
    return render(request, 'index.html')
