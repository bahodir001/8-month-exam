from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user_app.models import UserModel
from django.views.generic.edit import CreateView
from .models import UserModel


# class AccountForm(CreateView):
#     model = UserModel
#     fields = ['email', 'first_name', 'last_name', 'password']
#     form_class = UserModel


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model  = UserModel
        fields  = ['email','first_name','last_name']

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get('password1')
            password2 = cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                self.add_error('password2', 'Passwords do not match.')

            return cleaned_data

        def create_user(self):
            user = UserModel(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            user.set_password(self.cleaned_data['password1'])
            user.save()
            return user

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for _, field  in self.fields.items():
            field.widget.attrs.update({
                 'class':'text-light form-control form-control-lg',
            })


# class UserUpdateForm(forms.ModelForm):
#     password = forms.CharField(max_length=255, widget=forms.PasswordInput(), required=False)
#     password_confirmation = forms.CharField(max_length=255, widget=forms.PasswordInput(), required=False)
#
#     class Meta:
#         model = UserModel
#         fields = ["email", "first_name", "last_name"]
#
#     def clean(self):
#         cleaned_data = super().clean()
#
#         password = cleaned_data.get("password", "")
#         password_confirmation = cleaned_data.get("password_confirmation", "")
#
#         if password and password != password_confirmation:
#             raise ValidationError("Passwords should match")
#
#         return cleaned_data
#
#     def __init__(self, *args, **kwargs):
#         kwargs.pop("request", None)
#
#         super().__init__(*args, **kwargs)
#
#         for key, field in self.fields.items():
#             label = key.replace("_", " ").title()
#             field.widget.attrs.update(
#                 {
#                     "placeholder": label,
#                     "class": "text-light form-control form-control-lg"
#                 }
#             )
#             field.label = label

class UpdateAccountForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

