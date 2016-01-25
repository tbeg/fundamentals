from django import forms

class FundaLoginForm(forms.Form):
    funda_username = forms.CharField(label='Your Funda Username', max_length=100)
    funda_password = forms.CharField(label='Your Funda Password', max_length=100)