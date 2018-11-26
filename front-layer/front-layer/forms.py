from django import forms


class ListingForm(forms.Form):
    sample_name = forms.CharField(
        label='Name',
        max_length=50,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Sample name'}
        )
    )
    sample_description = forms.CharField(
        label='Description',
        max_length=1000,
        widget=forms.Textarea(
            attrs={'class':'form-control', 'placeholder':'Sample description'}
        )
    )
    price = forms.DecimalField(
        label='Price',
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class':'form-control', 'placeholder': '0.00'}
        )
    )

class MusicianForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=25,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Username'}
        )
    )
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'Password'}
        )
    )
    email = forms.EmailField(
        label='Email',
        max_length=25,
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'user@example.com'}
        )
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=25,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Username'}
        )
    )
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'Password'}
        )
    )
