from django import forms

class SearchForm(forms.Form):
    #a form to store the criterias for search query (case-insensitive, i.e. search if XX contain these words, regardless of the upper/lowercase)
    genderchoices = (('M', 'Male'), ('F', ' Female'), ('any', 'Any'))
    gender = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}),choices=genderchoices)
    jobtitle = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),label='jobtitle_wanted',required=True)
    passions = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),label='passion_wanted',required=True)

    #form-control is come from bootstrap
class RequestForm(forms.Form): #to store the input (can be used in sending request or accepting friend)
    usernamelist = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),label='usernamelist',required=True)
