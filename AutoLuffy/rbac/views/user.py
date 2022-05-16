from django.shortcuts import render, HttpResponse, redirect
from rbac.models import User
from django.urls import reverse
from rbac.forms.user import UserModelForm, UserEditModelForm, UserResetPasswordModelForm


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    user_queryset = User.objects.all()
    return render(request, 'rbac/user_list.html', {"user_queryset": user_queryset})


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    """
    编辑用户
    :param request:
    :param pk:要修改的角色ID
    :return:
    """
    role_obj = User.objects.filter(id=pk).first()
    if not role_obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UserEditModelForm(instance=role_obj)
        return render(request, "rbac/change.html", {'form': form})
    form = UserEditModelForm(data=request.POST, instance=role_obj)
    if form.is_valid():
        form.save()
        return redirect(reverse("rbac:user_list"))
    else:
        return render(request, "rbac/change.html", {'form': form})


def user_del(request, pk):
    """
    删除用户
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:user_list')
    if request.method == "GET":
        return render(request, 'rbac/user_del.html', {'cancel': origin_url})

    User.objects.filter(id=pk).delete()
    return redirect(origin_url)


def user_password_reset(request, pk):
    user_obj = User.objects.filter(id=pk).first()
    if not user_obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UserResetPasswordModelForm()
        return render(request, "rbac/change.html", {'form': form})
    form = UserResetPasswordModelForm(data=request.POST, instance=user_obj)
    if form.is_valid():
        form.save()
        return redirect(reverse("rbac:user_list"))
    else:
        return render(request, "rbac/change.html", {'form': form})
