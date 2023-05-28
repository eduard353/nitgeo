from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Profile
from .validators import validate_birth_date

User = get_user_model()


class DateInputCustom(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, options=None):
        if attrs is None:
            attrs = {}
        if options is None:
            options = {}
        attrs.update({'class': 'form-control mb-3',
                      'data-date-format': 'yyyy-mm-dd'})
        attrs.update(options)
        super().__init__(attrs=attrs)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']
        widgets = {
            'username': forms.TextInput(),
            'password1': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class PasswordSetForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]
        widgets = {
            'new_password1': forms.PasswordInput(),
            'new_password2': forms.PasswordInput()
        }

    def __init__(self, user, *args, **kwargs):
        super(PasswordSetForm, self).__init__(user, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ReactivationForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('User with this email does not exists')
        return email


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError('User with this email does not exists')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'date_of_birth', 'avatar', 'bio', 'info')

        labels = {
            'date_of_birth': 'Date of your Birth',
            'avatar': 'Avatar URL'
        }

        placeholders = {
            'avatar': 'Left empty to use gravatar',
            'bio': 'Write a short biography',
            'info': 'Enter some additional information'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control border border-4 mb-3',
                                      'placeholder': self.Meta.placeholders.get(field_name)})
        self.fields['date_of_birth'].widget = DateInputCustom()

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        try:
            validate_birth_date(data)
        except ValidationError as exception:
            self.add_error('date_of_birth', str(exception))
        return data
