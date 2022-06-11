from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

class LogForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UpdateUser(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea)
    picture = forms.FileField()

    