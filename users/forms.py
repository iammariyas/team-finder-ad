from django import forms

from .models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password', 'phone')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        data = self.cleaned_data
        user = User.objects.create_user(
            email=data['email'],
            name=data['name'],
            surname=data['surname'],
            password=data['password'],
            phone=data['phone'],
        )
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'about', 'phone', 'github_url', 'avatar')
