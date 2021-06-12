from django import forms
from .models import Downkey
from django.forms import ModelForm


""" class FileDawnloadModelForm(forms.ModelForm):
    class Meta:
        model = Downkey
        fields = ('sec_key',)

        widgets = {
            
            'sec_key': forms.TextInput(attrs={'class': 'form-control'}),
        }
 """
    

class FileDawnloadModelForm(forms.Form):
    class Meta:
        model = Downkey
        fields = '__all__'


class BlogForm(ModelForm):
    class Meta: 
        model = Downkey
        fields = '__all__'

        widgets = {
            'sec_key': forms.TextInput(attrs={'class': 'form-control'}),
        }
