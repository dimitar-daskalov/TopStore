from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from TopStore.accounts.models import Profile
from TopStore.shared.bootstrap_form_mixin import BootstrapFormMixin

UserModel = get_user_model()


class SingInForm(BootstrapFormMixin, forms.Form):
    user = None
    email = forms.EmailField(
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    def clean_password(self):
        try:
            self.user = authenticate(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
            )
        except:
            raise ValidationError('Email and/or password incorrect')

    def save(self):
        return self.user


class SingUpForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username')


class ProfileDetailsForm(BootstrapFormMixin, forms.ModelForm):
    profile_image = forms.ImageField(
        widget=forms.FileInput(),
    )

    class Meta:
        model = Profile
        fields = ('profile_image',)
