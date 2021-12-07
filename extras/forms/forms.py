from django import forms
from django.db import models
from django.forms import fields

from forms.models import ProductPlus, Product


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(label='E-mail')
    category = forms.ChoiceField(
        choices=[('question', 'Question'), ('other', 'Other')])
    subject = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea)


class ProductPlusForm(forms.ModelForm):
    class Meta:
        model = ProductPlus
        fields = ['title', 'description', 'price', 'featured']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
