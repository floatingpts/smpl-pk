from django import forms


class ListingForm(forms.Form):
    

class MusicianForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    


