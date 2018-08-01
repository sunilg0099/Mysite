from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='username', 
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'please enter user name'}))
    password = forms.CharField(label='password', 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Please enter your password'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Username or password is incorrect')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='username', 
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter 3-30 usernames'}))
    email = forms.EmailField(label='mailbox', 
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'please input your email'}))
    password = forms.CharField(label='password', 
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Please enter your password'}))
    password_again = forms.CharField(label='Enter the password again', 
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter the password again'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The mailbox already exists')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('Inconsistent password entered twice')
        return password_again
