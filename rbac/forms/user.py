from django import forms
from rbac.models import User
from django.core.exceptions import ValidationError


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码',
                                       widget=forms.PasswordInput())

    # 统一给字段添加样式
    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['name', 'password', 'confirm_password', 'email']
        widgets = {
            'password': forms.widgets.PasswordInput(),
        }

    def clean_confirm_password(self):
        """
        检测两次输入密码是否一致
        :return:
        """
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('confirm_password')
        if password != r_password:
            raise ValidationError('两次输入密码不一致')
        return r_password


class UserEditModelForm(forms.ModelForm):
    # 统一给字段添加样式
    def __init__(self, *args, **kwargs):
        super(UserEditModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['name', 'email']


class UserResetPasswordModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码',widget=forms.PasswordInput())

    # 统一给字段添加样式
    def __init__(self, *args, **kwargs):
        super(UserResetPasswordModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.widgets.PasswordInput(),
        }
