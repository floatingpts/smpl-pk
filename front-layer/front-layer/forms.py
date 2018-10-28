from django import forms


class ListingForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    description = forms.TextField(label='Description', max_length=1000)
    price = forms.DecimalField(label='Price', max_digits=5, decimal_places=2)
    num_samples = forms.IntegerField('Number of Samples', default=0)

class Musician(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    password = forms.CharField(label='Password', max_length=1000)
    


