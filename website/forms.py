from django import forms

class QueryForm(forms.Form):
    package = forms.IntegerField()