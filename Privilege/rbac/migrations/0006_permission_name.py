# Generated by Django 3.2 on 2022-05-07 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_permission_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=32, null=True, verbose_name='URL的别名'),
        ),
    ]
