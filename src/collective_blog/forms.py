# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from models import Comment
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    login = forms.CharField(label='Login', required=True, error_messages = {'already_exists': 'Пользователь с таким именем уже существует'})
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    conf_password = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput, error_messages = {'pass_donotmatch': 'Введенные пароли не совпадают'})
    captcha=CaptchaField()

    def clean_login(self):
        check_usr = User.objects.filter(username = self.cleaned_data['login'])
        if check_usr.count() == 1:
            raise ValidationError(self.fields['login'].error_messages['already_exists'])
        return self.cleaned_data['login']

    def clean_conf_password(self):
       if self.cleaned_data['conf_password'] != self.cleaned_data['password']:
          raise ValidationError(self.fields['conf_password'].error_messages['pass_donotmatch'])
       return self.cleaned_data['conf_password']

class LoginForm(forms.Form):

    login = forms.CharField(label='Login', required=True,
                            error_messages = {'not_exists':'Такого пользователя не существует', 'wrong_pass':'Вы ввели неправильный пароль'})
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    captcha=CaptchaField()

    def clean_password(self):
        print self.cleaned_data
        check_usr = User.objects.filter(username = self.cleaned_data['login'])
        if check_usr.count() == 0:
            raise ValidationError(self.fields['login'].error_messages['not_exists'])
        else:
            if not check_usr[0].check_password(self.cleaned_data['password']):
                raise ValidationError(self.fields['login'].error_messages['wrong_pass'])
        return self.cleaned_data['password']

class AddCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class' : 'expand'}))

class AddPostForm(forms.Form):
    title = forms.CharField(label='title', required=True)
    text=forms.CharField(label='text', required=False, widget=forms.Textarea(attrs={'rows': '15'}))