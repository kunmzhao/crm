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



## 二. 增删改查组件

## 三. CRM业务组件