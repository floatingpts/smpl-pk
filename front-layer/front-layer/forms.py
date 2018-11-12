from django import forms


class ListingForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    description = forms.TextField(label='Description', max_length=1000)
    price = models.DecimalField(label='Price', max_digits=5, decimal_places=2)


class MusicianForm(forms.Form):
    username = forms.CharField(label='Username', max_length=25)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=100)
    


