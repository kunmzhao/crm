from django.forms import ModelForm
from web import models


class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'
            filed.widget.attrs['placeholder'] = filed.label
