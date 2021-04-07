from django import forms

class SearchForm(forms.Form):
    #TBD
    genderchoices = (('M', 'Male'), ('F', ' Female'), ('any', 'Any'))
    gender = forms.ChoiceField(widget=forms.Select(),choices=genderchoices)
    jobtitle = forms.CharField(label='jobtitle_wanted',required=True)
    passions = forms.CharField(label='passion_wanted',required=True)
    
class RequestForm(forms.Form):
    usernamelist = forms.CharField(label='usernamelist',required=True)
