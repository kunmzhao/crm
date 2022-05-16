from django import forms
from django.core.exceptions import ValidationError

from app01.models import Host


class HostModelForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(HostModelForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

