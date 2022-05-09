from django import forms
from rbac.models import Menu, Permission
from django.utils.safestring import mark_safe

ICON_LIST = [
    ['fa fa-address-book', '<i class="fa fa-address-book" aria-hiddern=True></i>'],
    ['fa fa-bandcamp', '<i class="fa fa-bandcamp" aria-hiddern=True></i>'],
    ['fa fa-drivers-license-o', '<i class="fa fa-drivers-license-o" aria-hiddern=True></i>'],
    ['fa fa-quora', '<i class="fa fa-quora" aria-hiddern=True></i>'],
    ['fa fa-snowflake-o', '<i class="fa fa-snowflake-o" aria-hiddern=True></i>'],
    ['fa fa-thermometer-0', '<i class="fa fa-thermometer-0" aria-hiddern=True></i>'],
    ['fa fa fa-user-circle', '<i class="fa fa-user-circle" aria-hiddern=True></i>'],
    ['fa fa-area-chart', '<i class="fa fa-area-chart" aria-hiddern=True></i>'],
    ['fa fa-bank', '<i class="fa fa-bank" aria-hiddern=True></i>'],
]
for item in ICON_LIST:
    item[1] = mark_safe(item[1])


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.RadioSelect(
                choices=ICON_LIST
            )
        }
        labels = {
            'title': '菜单名称'
        }


class SecondMenuModelForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['title', 'url', 'name', 'menu']

    def __init__(self, *args, **kwargs):
        super(SecondMenuModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
