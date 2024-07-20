from django import forms
from .models import NetworkElement, Product

class NetworkElementForm(forms.ModelForm):
    class Meta:
        model = NetworkElement
        fields = ['name', 'email', 'country', 'city', 'street', 'house_number', 'supplier', 'debt']
        widgets = {
            'debt': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['debt'].required = False  # Устанавливаем debt как необязательное поле

    def clean(self):
        cleaned_data = super().clean()
        supplier = cleaned_data.get('supplier')
        debt = cleaned_data.get('debt')

        # Проверяем и устанавливаем значение debt, если оно не задано
        if supplier and debt is None:
            cleaned_data['debt'] = 0  # Или любое другое значение по умолчанию

        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'model', 'release_date', 'network_element']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['network_element'].queryset = NetworkElement.objects.all()