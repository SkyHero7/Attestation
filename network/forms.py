from django import forms
from .models import NetworkElement

class NetworkElementForm(forms.ModelForm):
    class Meta:
        model = NetworkElement
        fields = '__all__'