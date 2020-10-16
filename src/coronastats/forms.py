from django import forms

class CountryForm(forms.Form):
    choices = [('new_cases', 'New cases'), ('total_cases', 'Total cases'), ('new_deaths', 'New deaths'), ('total_deaths', 'Total deaths')]
    country = forms.CharField()
    choice = forms.ChoiceField(choices = choices, label='Type of chart')
    # another_country = forms.CharField(required=False, label = 'Add another country')

class CountryPageForm(forms.Form):
	country = forms.CharField()
