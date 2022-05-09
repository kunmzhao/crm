from django.shortcuts import render, HttpResponse, redirect
from rbac.models import Menu, Permission
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm
from django.urls import reverse
from rbac.service.urls import memory_reverse


def menu_list(request):
    """
    菜单列表
    :param request:
    :return:
    """
    menu_queryset = Menu.objects.all()
    # 一级菜单
    menu_id = request.GET.get('mid')
    is_exist = Menu.objects.filter(id=menu_id).exists()
    if not is_exist:
        menu_id = None
    # 二级菜单
    second_menu_id = request.GET.get('sid')
    is_exist = Permission.objects.filter(id=second_menu_id).exists()
    if not is_exist:
        second_menu_id = None
    if menu_id:
        second_menus = Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []
    # 权限
    if second_menu_id:
        permissions = Permission.objects.filter(pid=second_menu_id)
    else:
        permissions = []
    return render(request, 'rbac/menu_list.html', {
        "menu_queryset": menu_queryset,
        'menu_id': menu_id,
        "second_menus": second_menus,
        "second_menu_id": second_menu_id,
        "permissions": permissions,
    })


def menu_add(request):
    """
    添加菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    """
    编辑菜单
    :param request:
    :param pk:
    :return:
    """
    menu_obj = Menu.objects.filter(id=pk).first()
    if not menu_obj:
        return HttpResponse('菜单不存在')
    if request.method == "GET":
        form = MenuModelForm(instance=menu_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(data=request.POST, instance=menu_obj)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, pk):
    """
    删除菜单
    :param request:
    :param pk:
    :return:
    """
    menu_obj = Menu.objects.filter(id=pk).first()
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if not menu_obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        return render(request, 'rbac/menu_del.html', {'cancel': origin_url})
    Menu.objects.filter(id=pk).delete()
    return redirect(origin_url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id:
    :return:
    """
    menu_object = Menu.objects.filter(id=menu_id).first()
    if request.method == "GET":
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/change.html', {"form": form})
    form = SecondMenuModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param menu_id:
    :return:
    """
    second_menu_obj = Permission.objects.filter(id=pk).first()
    if not second_menu_obj:
        return HttpResponse('二级菜单不存在')
    if request.method == "GET":
        form = SecondMenuModelForm(instance=second_menu_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(data=request.POST, instance=second_menu_obj)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
    """

    :param request:
    :param menu_id:
    :return:
    """
    second_menu_obj = Permission.objects.filter(id=pk).first()
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if not second_menu_obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        return render(request, 'rbac/menu_del.html', {'cancel': origin_url})
    Permission.objects.filter(id=pk).delete()
    return redirect(origin_url)
