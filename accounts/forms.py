from datetime import date

from django import forms
from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Profile


class DateInput(forms.DateInput):
    input_type = 'date'


#class ImageWidget(forms.widgets.ClearableFileInput):
#    template_name = "accounts/widgets/image_widget.html"


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "django/forms/widgets/file.html"


#class ImageWidget(forms.Form):
#    profile_image = forms.FileField(widget=FileInput)


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    date_of_birth = forms.DateField(
        label='Date of birth',
        widget=DateInput
    )

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth',)

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > date.today():
            raise ValidationError("Wrong date of birth!")
        return date_of_birth


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class UserProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(
        label='Profile image',
        required=False,
        widget=ImageWidget(
            attrs={
                'class': 'form-control',
            }
        )
    )
    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows':7,
                'cols':15,
                'data-html': True,
                'placeholder': 'Write something about you.'
            }
        )
    )



    class Meta:
        model = Profile
        fields = ('profile_image', 'bio',)

