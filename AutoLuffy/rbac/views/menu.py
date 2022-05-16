from django.shortcuts import render, HttpResponse, redirect
from rbac.models import Menu, Permission, User, Role
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, \
    MultiAddPermissionForm, MultiEditPermissionForm
from rbac.service.urls import memory_reverse
from rbac.service.routers import get_all_url_dict
from collections import OrderedDict
from django.forms import formset_factory
from django.conf import settings
from django.utils.module_loading import import_string


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


def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu_obj = Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_obj:
            return HttpResponse('二级菜单不存在')
        # 添加权限表中的pid
        form.instance.pid = second_menu_obj
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/chang.html', {'form': form})


def permission_edit(request, pk):
    """
    修改权限
    :param request:
    :param second_menu_id:
    :return:
    """
    permission_obj = Permission.objects.filter(id=pk).first()
    if not permission_obj:
        return HttpResponse("权限不存在")
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(data=request.POST, instance=permission_obj)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/chang.html', {'form': form})


def permission_del(request, pk):
    """
    删除权限
    :param request:
    :param second_menu_id:
    :return:
    """
    permission_obj = Permission.objects.filter(id=pk).first()
    origin_url = memory_reverse(request, 'rbac:menu_list')
    if not permission_obj:
        return HttpResponse('权限不存在')
    if request.method == 'GET':
        return render(request, 'rbac/menu_del.html', {'cancel': origin_url})
    Permission.objects.filter(id=pk).delete()
    return redirect(origin_url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')
    generate_form_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_form_class = formset_factory(MultiEditPermissionForm, extra=0)
    generate_formset = None
    update_formset = None
    # 批量增加
    if request.method == 'POST' and post_type == 'generate':
        formset = generate_form_class(request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            # 批量添加数据到数据库
            if not has_error:
                Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset = formset
    # 批量更新
    if request.method == 'POST' and post_type == 'update':
        formset = update_form_class(request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            print(formset.total_form_count())
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset
    # 1. 获取项目中的所有URL
    all_url_dict = get_all_url_dict()
    router_name_set = set(all_url_dict.keys())

    # 2.获取数据库中的所有URL
    permissions_queryset = Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    for row in permissions_queryset:
        permission_dict[row['name']] = row
    permission_name_set = set(permission_dict.keys())

    # 防止数据库和路由中name一样但是url不一致
    for name, value in permission_dict.items():
        router_url_dict = all_url_dict.get(name)
        if not router_url_dict:
            continue
        if router_url_dict['url'] != all_url_dict[name].get('url'):
            value['url'] = '路由和数据库不一致！'

    # 3.1 增加到数据库的权限
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_form_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # 3.2 从数据库中删除的权限
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 更新到到数据库的权限
    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        update_formset = update_form_class(
            initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    return render(request, 'rbac/multi_permissions.html', {
        'generate_formset': generate_formset,
        'delete_row_list': delete_row_list,
        'update_formset': update_formset,
    })


def multi_permissions_del(request, pk):
    """
    删除权限
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/menu_del.html', {'cancel': url})
    Permission.objects.filter(id=pk).delete()
    return redirect(url)


def distribute_permissions(request):
    """
    权限的分配
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    user_obj = import_string(settings.RBAC_USER_MODEL_CLASS).objects.filter(id=uid).first()
    role_obj = Role.objects.filter(id=rid).first()

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        if not user_obj:
            return HttpResponse('请选择用户,再分配角色')
        user_obj.roles.set(role_id_list)
    if request.method == "POST" and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_obj:
            return HttpResponse('请选择角色，再分配权限')
        role_obj.permissions.set(permission_id_list)
    if not user_obj:
        uid = None

    if uid:
        # 获取当前用户所拥有的所有角色
        user_has_roles = user_obj.roles.all()
        # 获取当前用户所拥有的权限
        user_has_permissions = user_obj.roles.filter(permissions__id__isnull=False).values('permissions__id').distinct()
    else:
        user_has_roles = []
        user_has_permissions = []
    user_has_roles_dict = {item.id: item for item in user_has_roles}
    user_has_permissions_dict = {item['permissions__id']: None for item in user_has_permissions}

    flag = False
    if not role_obj:
        rid = None
        role_has_permissions = []
    # 选中角色的时候，权限优先显示对应角色的权限
    else:
        role_has_permissions = role_obj.permissions.all()
        flag = True
    role_has_permissions_dict = {item.id: None for item in role_has_permissions}

    # 获取所有用户
    all_user_list = import_string(settings.RBAC_USER_MODEL_CLASS).objects.all()

    # 获取所有的角色
    all_role_list = Role.objects.all()

    # 获取所有的一级菜单
    all_menu_list = Menu.objects.all().values('id', 'title')
    all_menu_dict = {}
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item

    # 获取所有的二级菜单
    all_second_menu_list = Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    all_second_menu_dict = {}
    for item in all_second_menu_list:
        item['children'] = []
        all_second_menu_dict[item['id']] = item
        all_menu_dict[item['menu_id']]['children'].append(item)

    # 获取所有的三级菜单
    all_permissions_list = Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    for item in all_permissions_list:
        pid = item['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(item)
    return render(request, 'rbac/distibute_permissions.html', {
        'user_list': all_user_list,
        'role_list': all_role_list,
        'all_menu_list': all_menu_list,
        'uid': uid,
        'user_has_roles_dict': user_has_roles_dict,
        'user_has_permissions_dict': role_has_permissions_dict if flag else user_has_permissions_dict,
        'rid': rid
    })
