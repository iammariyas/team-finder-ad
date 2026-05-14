from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import User


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=124, label='Имя')
    surname = forms.CharField(max_length=124, label='Фамилия')
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class LoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'about', 'phone', 'github_url', 'avatar')


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Текущий пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение нового пароля'
