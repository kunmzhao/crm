from django.shortcuts import render, HttpResponse, redirect

from app01.models import User, Host, Department
from app01.forms.user import UserModelForm, UserUpdateModelForm, ResetPasswordUserModelForm
from rbac.service.urls import memory_reverse


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    user_queryset = User.objects.all()
    return render(request, 'user_list.html', {
        'user_queryset': user_queryset
    })


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    """
    编辑用户
    :param request:
    :param pk:
    :return:
    """
    user_obj = User.objects.filter(id=pk).first()
    if not user_obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UserUpdateModelForm(instance=user_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = UserUpdateModelForm(data=request.POST, instance=user_obj)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_del(request, pk):
    """
    删除用户
    :param request:
    :param pk:
    :return:
    """
    origin_url = memory_reverse(request, 'user_list')
    if request.method == 'GET':
        return render(request, 'rbac/menu_del.html', {'cancel': origin_url})
    User.objects.filter(id=pk).delete()
    return redirect(origin_url)


def user_reset_pwd(request, pk):
    """
    重置密码
    :param request:
    :param pk:
    :return:
    """
    pass
