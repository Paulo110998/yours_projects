from django import forms

class Checkbox(forms.Form):
    metodo = forms.ChoiceField(choices=(('POST', 'POST'), ('GET', 'GET')), widget=forms.RadioSelect)
