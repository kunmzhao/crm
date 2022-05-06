## 一. 权限组件

### 1.1 权限组件介绍

1. 为什么需要权限控制

   ```
   针对不同的用户进行不同权限的操作
   ```

   - 你能看到同事的薪水吗？老板可以
   - 你能和女神玩耍吗？马化腾可以

2. 为什么要开发权限组件

   ```
   基本所有的系统都会有关于权限的操作
   ```

3. Web中什么是权限？

   ```
   一个URL就是一个权限
   
   不同的URL对应不同的请求，而一个请求就对应一个应答，你有多少权限，其实就是你有多少个能访问的URL
   ```

### 1.2 第一版表结构设计

- 用户表
- 权限表
- 用户权限关系表

用户表和权限表是一个多对多的关系

在代码中就是两个类，三张表

```python
# 创建权限类
class Privilege(models.Model):
    id = models.AutoField(auto_increment=True, primary_key=True)
    urls = models.CharField(max_length=128)


# 创建用户类
class User(models.Model):
    id = models.AutoField(auto_increment=True, primary_key=True)
    name = models.CharField(max_length=32)
    urls = models.ManyToManyField(to='Privilege', null=True)
```

缺点：

对同类的用户做权限的增删改查太麻烦，比如张三李四都是主管，他们拥有相同的权限，当对销售专管做权限操作的时候，张三李四拥有的权限都要修改，我们可以将销售主管这个角色抽离出来，将角色分配给人，将权限分配给角色



### 1.3 第二版表结构设计

- 用户表
- 权限表
- 角色表
- 用户角色关系表（多对多）
- 角色权限表（多对多）

在代码中就是三个类，五张表

```python
class Permission(models.Model):
    """
    权限类
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=128, verbose_name='含正则的URL')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='拥有的所有权限', blank=True)

    def __str__(self):
        return self.title


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.CharField(max_length=32, verbose_name='邮箱')
    roles = models.ManyToManyField(to='Role', verbose_name='拥有的所有角色', blank=True)

    def __str__(self):
        return self.name

```

### 1.4 web应用

为了更好的实现权限组键，我们在创建一个web的应用，将业务实现在该应用中

销售系统的业务代码实现

### 1.5 将web中实现的权限的录入权限表中

1. 权限表

<img src="picture/image-20220506134402502.png" alt="image-20220506134402502" style="zoom:50%;" />

2. 角色表

   <img src="picture/image-20220506135443904.png" alt="image-20220506135443904" style="zoom:50%;" />

3. 角色权限关系表
   <img src="picture/image-20220506135731126.png" alt="image-20220506135731126" style="zoom:50%;" />

4. 用户表
   <img src="picture/image-20220506135952666.png" alt="image-20220506135952666" style="zoom:50%;" />

5. 用户角色表
   <img src="picture/image-20220506140053907.png" alt="image-20220506140053907" style="zoom:50%;" />

### 1.6 快速完成基本权限控制

设计思路：
<img src="picture/image-20220506142231301.png" alt="image-20220506142231301" style="zoom:50%;" />

1. 用户第一次请求从登录页面开始
   1. 用户发起登录页面的GET请求
   2. 服务端响应登录页面
2. 用户将登陆信息通过POST方式发送
3. 获取当前用户的所有权限信息并放入session中
4. 用户再次发起请求，请求中就会有该用户的所有权限信息，在中间件中判断用户访问的URL是否在该用户的权限中

知识点：

1. ORM:跨表查询
2. 中间件
   process_request函数中返回None则可以继续执行下面的中间件，否则返回
3. session
   设置中间件，获取中间件
4. DJango在寻找模板文件的时候优先去最外层目录照templates文件夹，如果没有找到，就会按照app注册的顺序去子项目的templates中寻找
5. 正则匹配

模板函数：

```python
from django.shortcuts import HttpResponse, render, redirect
# TBD: 不要跨项目引入
from rbac.models import User


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username, password)
    user_obj = User.objects.filter(name=username, password=password).first()
    if not user_obj:
        # 用户名或者密码不正确
        return render(request, 'login.html', {"info": '用户名或者密码不正确'})
    # 登陆成功，查找该用户的所有权限
    """
    本次查询垮了两张表，注意去重和为空的筛选
    """
    permission_queryset = user_obj.roles.filter(permissions__isnull=False).values('permissions__id',                                                                                																																							'permissions__url').distinct()
    # 获取权限中的所有URL
    permission_list = [item['permissions__url'] for item in permission_queryset]

    # 将权限信息写入session中
    request.session['luffy_permission_url_list'] = permission_list
    return redirect('/customer/list/')

```

中间件

```python
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse


class CheckPermission(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        验证用户权限
        :param request:
        :return:
        """
        # 白名单
        valid_url_list = [
            '/login/',
            '/admin/*'
        ]
        # 获取当前请求的url
        current_url = request.path_info

        # 判断url是否在白名单里面
        for item in valid_url_list:
            item = "^%s$" % item
            if re.match(item, current_url):
                return None

        # 获取当前用户session中的权限
        permission_list = request.session['luffy_permission_url_list']
        if not permission_list:
            return HttpResponse('为获取用户权限信息，请登录')

        # 判断用户当前请求是否在session中
        flag = False
        for url in permission_list:
            # 匹配应该严格
            reg = "^%s$" % url
            # 用户拥有权限
            if re.match(reg, current_url):
                flag = True
                break

        if not flag:
            return HttpResponse('无权访问')

```



## 二. 增删改查组件

## 三. CRM业务组件