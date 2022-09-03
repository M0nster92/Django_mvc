from django import forms

class ArticleForm(forms.Form):
    name = forms.CharField()
    content = forms.CharField()

    def clean_name(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        return name