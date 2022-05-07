from django.shortcuts import render, HttpResponse, redirect
from rbac.models import Role
from django.urls import reverse
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = Role.objects.all()
    return render(request, 'rbac/role_list.html', {"role_queryset": role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk:要修改的角色ID
    :return:
    """
    role_obj = Role.objects.filter(id=pk).first()
    if not role_obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=role_obj)
        return render(request, "rbac/change.html", {'form': form})
    form = RoleModelForm(data=request.POST, instance=role_obj)
    if form.is_valid():
        form.save()
        return redirect(reverse("rbac:role_list"))
    else:
        return render(request, "rbac/change.html", {'form': form})


def role_del(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == "GET":
        return render(request, 'rbac/role_del.html', {'cancel': origin_url})

    Role.objects.filter(id=pk).delete()
    return redirect(origin_url)
