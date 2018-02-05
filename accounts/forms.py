# coding=utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from siw.jqxwidgets import JqxPasswordInput, JqxTextInput, JqxEmailInput


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=JqxTextInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    password1 = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    password2 = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    email = forms.EmailField(widget=JqxEmailInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=JqxTextInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    password = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))

    class Meta:
        model = User
        fields = ('username', 'password')


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=JqxEmailInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    new_password2 = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    new_password1 = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
    new_password2 = forms.CharField(widget=JqxPasswordInput(jqxattrs={'height': 30, 'width': 350, 'minLength': 1}))
