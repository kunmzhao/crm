from django.shortcuts import render, HttpResponse, redirect

from app01.models import User, Host, Department
from app01.forms.host import HostModelForm
from rbac.service.urls import memory_reverse


def host_list(request):
    """
    主机列表
    :param request:
    :return:
    """
    host_queryset = Host.objects.all()
    return render(request, 'host_list.html', {
        'host_queryset': host_queryset
    })


def host_add(request):
    """
    添加主机
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = HostModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = HostModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def host_edit(request, pk):
    """
    编辑主机
    :param request:
    :param pk:
    :return:
    """
    host_obj = Host.objects.filter(id=pk).first()
    if not host_obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = HostModelForm(instance=host_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = HostModelForm(data=request.POST, instance=host_obj)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def host_del(request, pk):
    """
    删除主机
    :param request:
    :param pk:
    :return:
    """
    origin_url = memory_reverse(request, 'user_list')
    if request.method == 'GET':
        return render(request, 'rbac/menu_del.html', {'cancel': origin_url})
    Host.objects.filter(id=pk).delete()
    return redirect(origin_url)


def user_reset_pwd(request, pk):
    """
    重置密码
    :param request:
    :param pk:
    :return:
    """
    pass
