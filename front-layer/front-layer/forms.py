from django import forms


class ListingForm(forms.Form):
    

class Musician(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    


