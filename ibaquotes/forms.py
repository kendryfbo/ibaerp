from django import forms
from ibaquotes.models.product import Product

class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = ['pdid', 'name', 'descr1', 'descr2', 'detail', 'remarks', 'price', 'weight', 'harmonizedcode']

        widgets = {
            'pdid': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'descr1': forms.TextInput(attrs={'class': 'form-control'}),
            'descr2': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'harmonizedcode': forms.TextInput(attrs={'class': 'form-control'})
        }