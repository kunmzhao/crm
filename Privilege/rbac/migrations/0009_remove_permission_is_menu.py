# Generated by Django 3.2 on 2022-05-09 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0008_alter_menu_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='is_menu',
        ),
    ]
