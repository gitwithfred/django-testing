from django.forms import ModelForm

from . import models


class MainModelForm(ModelForm):
    class Meta:
        model = models.MainModel
        fields = '__all__'
