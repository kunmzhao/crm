rbac组件的使用文档

1. 将rbac组件拷贝的项目中

2. 将rbac目录migrations中的数据记录删除

3. 业务系统中表结构的设计
    
    业务表中的用户表需要继承rbac组件中的用户表
  
    ​	rbac/models.py
    
    ```
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
    
        class Meta:
            abstract = True
    ```
    
    App01/models.py
    
    ```
    class User(rbacUser):
        """
        用户表
        """
        phone = models.CharField(max_length=32, verbose_name='手机号')
        level_choices = (
            (1, 'T1'),
            (2, 'T2'),
            (3, 'T3'),
        )
        level = models.IntegerField(choices=level_choices, verbose_name='级别')
        depart = models.ForeignKey(to='Department', verbose_name='部门')
    ```
    
    
    
    4. 将业务中用户表结构的路径写入配置文件setting.py中
    
       ```python
       # 业务中的用户表
       RBAC_USER_MODEL_CLASS = 'app01.models.User'
       ```
    
       用于rbac分配权限的时候，读取业务表中的用户信息
    
    5. 业务逻辑开发
    
       将所有的路由都设置一个name,如：
    
       ```python
       url('login/', account.login, name='login'),
       url('logout/', account.logout, name='logout'),
       url('index/', account.index, name='index'),
       ```
    
       用于反向生成url及控制力度到按钮的权限
    
    6. 权限信息的录入
    
       1. 在URL中添加权限的路由
    
       ```python
       url('rbac/', include(('rbac.urls', 'rbac'), namespace='rbac')),
       ```
    
       2. rbac提供的地址进行操作
    
       ```python
       http://127.0.0.1:8000/rbac/role/list/
       http://127.0.0.1:8000/rbac/menu/list/
       http://127.0.0.1:8000/rbac/distribute/permissions/
       ```
    
       3. 自动发现时排除的权限
    
          ```
          # 配置URL查找的白名单
          AUTO_DISCOVER_EXCLUDE = [
              '/admin/.*',
              '/login/',
              '/logout/',
              '/index/'
          ]
          ```
    
          
    
    7. 编写用户登录逻辑(权限初始化)
       示例：
    
       ```python
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
       ```
    
       相关的配置在setting.py
    
       ```
       # 权限在session中的key
       PERMISSION_SESSION_KEY = 'luffy_permission_url_list_key'
       # 菜单在session中的key
       MENU_SESSION_KEY = 'luffy_menu_url_list_key'
       ```
    
       
    
    8. 编写首页index业务
       相关的配置在setting.py
    
       ```
       # 需要登录验证，但无序权限的名单
       NO_PERMISSION_LIST = [
           '/logout/',
           '/index/'
       ]
       ```
    
    9. 通过中间件进行权限校验
       将中间键添加到项目中
    
       ```
       MIDDLEWARE = [
           'django.middleware.security.SecurityMiddleware',
           'django.contrib.sessions.middleware.SessionMiddleware',
           'django.middleware.common.CommonMiddleware',
           'django.middleware.csrf.CsrfViewMiddleware',
           'django.contrib.auth.middleware.AuthenticationMiddleware',
           'django.contrib.messages.middleware.MessageMiddleware',
           'django.middleware.clickjacking.XFrameOptionsMiddleware',
           'rbac.middleware.rbac.RbacMiddleware'
       ]
       ```
    
       权限校验的白名单配置（无需登录就可以访问的URL）
    
       ```
       # 配置访问URL的白名单
       VALID_URL_LIST = [
           '/login/',
           '/admin/*'
       ]
       ```
    
    10. 控制力度到按钮
    
        ```htnl
        {% load rbac %}
        
        {% if request|has_permission:'host_add' %}
                        <a class="btn btn-default" href="{% memory_url request 'host_add' %}">
                            <i class="fa fa-plus-square" aria-hidden="true"></i> 添加主机
                        </a>
                    {% endif %}
        ```
    
        
    
    总结：希望在任意的系统中使用该权限组件，作为开发者
    
    1. 用户登录，注销和首页
    
    2. 项目的业务逻辑
       开发时灵活设置layout.html中的两个inclusion_tag，开发时去掉，上线时恢复
    
       ```html
       <div class="left-menu">
               <div class="menu-body">
                   {% multi_menu request %}
               </div>
           </div>
           <div class="right-body">
               <div>
                   {% url_record request %}
               </div>
               {% block content %} {% endblock %}
           </div>
       ```
    
    3. 权限的录入
    
    4. 配置信息
    
       ```
       MIDDLEWARE = [
           'django.middleware.security.SecurityMiddleware',
           'django.contrib.sessions.middleware.SessionMiddleware',
           'django.middleware.common.CommonMiddleware',
           'django.middleware.csrf.CsrfViewMiddleware',
           'django.contrib.auth.middleware.AuthenticationMiddleware',
           'django.contrib.messages.middleware.MessageMiddleware',
           'django.middleware.clickjacking.XFrameOptionsMiddleware',
           'rbac.middleware.rbac.RbacMiddleware'
       ]
       
       # # -----权限相关配置-----
       # 业务中的用户表
       RBAC_USER_MODEL_CLASS = 'app01.models.User'
       # 权限在session中的key
       PERMISSION_SESSION_KEY = 'luffy_permission_url_list_key'
       # 菜单在session中的key
       MENU_SESSION_KEY = 'luffy_menu_url_list_key'
       # 配置访问URL的白名单
       VALID_URL_LIST = [
           '/login/',
           '/admin/*'
       ]
       # 需要登录验证，但无序权限的名单
       NO_PERMISSION_LIST = [
           '/logout/',
           '/index/'
       ]
       # 配置URL查找的白名单
       AUTO_DISCOVER_EXCLUDE = [
           '/admin/.*',
           '/login/',
           '/logout/',
           '/index/'
       ]
       ```
    
       
    
    
    
    