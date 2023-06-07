from django.forms import forms
from catalog.models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__al__'