from django import forms
from ibaquotes.models.product import Product
from ibaquotes.models.client import Client

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

class CreateClientForm(forms.ModelForm):

    class Meta:
        model= Client
        fields= ['username','cfname','clname','cemail','company','newsletter','address','zipcode','city','country','domain','phone']
    
        widgets = {
            'username': forms.TextInput(attrs={'cclass': 'form-control'}),
            'cfname': forms.TextInput(attrs={'cclass': 'form-control'}),
            'clname': forms.TextInput(attrs={'cclass': 'form-control'}),
            'cemail': forms.TextInput(attrs={'cclass': 'form-control'}),
            'company': forms.TextInput(attrs={'cclass': 'form-control'}),
            'newsletter': forms.TextInput(attrs={'cclass': 'form-control'}),
            'address': forms.TextInput(attrs={'cclass': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'cclass': 'form-control'}),
            'city': forms.TextInput(attrs={'cclass': 'form-control'}),
            'country': forms.TextInput(attrs={'cclass': 'form-control'}),
            'domain': forms.TextInput(attrs={'cclass': 'form-control'}),
            'phone': forms.TextInput(attrs={'cclass': 'form-control'}),
        }
    