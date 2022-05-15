from django import forms
from django.core.exceptions import ValidationError

from app01.models import User


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = User
        fields = ['name', 'password', 'confirm_password', 'email', 'phone', 'level', 'depart']

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('两次输入密码不一致')
        return confirm_password


class UserUpdateModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'level', 'depart']

    def __init__(self, *args, **kwargs):
        super(UserUpdateModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'


class ResetPasswordUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = User
        fields = ['password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(ResetPasswordUserModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('两次输入密码不一致')
        return confirm_password
