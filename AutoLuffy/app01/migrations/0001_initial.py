# Generated by Django 3.2 on 2022-05-14 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='部门')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.CharField(max_length=32, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=32, verbose_name='手机号')),
                ('level', models.IntegerField(choices=[(1, 'T1'), (2, 'T2'), (3, 'T3')], verbose_name='级别')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.department', verbose_name='部门')),
                ('roles', models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='拥有的所有角色')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.department', verbose_name='归属部门')),
            ],
        ),
    ]
