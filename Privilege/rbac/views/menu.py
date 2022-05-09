from django.shortcuts import render, HttpResponse, redirect
from rbac.models import Menu
from rbac.forms.menu import MenuModelForm
from django.urls import reverse
from rbac.service.urls import memory_reverse


def menu_list(request):
    """
    菜单列表
    :param request:
    :return:
    """
    menu_queryset = Menu.objects.all()
    # 注意前后端数据类型
    menu_id = int(request.GET.get('mid', 1))
    return render(request, 'rbac/menu_list.html', {
        "menu_queryset": menu_queryset,
        'menu_id': menu_id,
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
