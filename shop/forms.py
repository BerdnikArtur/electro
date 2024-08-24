from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Search here'}))
    category = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class': 'input-select'}))

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(0, 'category')] + [(cat.pk, cat.name) for cat in categories]

class FiltersAside(forms.Form):
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
    brand = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    _categories_cache = None

    def __init__(self, *args, **kwargs):
        super(FiltersAside, self).__init__(*args, **kwargs)
        if FiltersAside._categories_cache is None:
            FiltersAside._categories_cache = list(Category.objects.all()[:4])
        categories = FiltersAside._categories_cache

        self.fields['category'].choices = [(str(category.pk), category.name) for category in categories]#[(str(i.pk), str(i.name)) for i in Category.objects.all()[:4]]
        self.fields['brand'].choices = [
            ('SAMSUNG', 'SAMSUNG'),
            ('LG', 'LG'),
            ('SONY', 'SONY'),
            ('POCO', 'POCO'),
            ('NVIDIA', 'NVIDIA'),
            ('AMD', 'AMD'),
        ]

    price__min = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'price-min', 'type': 'number'}))
    price__max = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'price-max', 'type': 'number'}))
    sort_by = forms.ChoiceField(choices=(('count_of_selled', 'Popular'), ('price', 'Price'), ('-time_updated', 'Hot Deals'),), widget=forms.Select(attrs={'class': 'input-select'}))

