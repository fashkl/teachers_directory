from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    password = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = User
        fields = ("username", "password")


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    password1 = forms.CharField(
        label="Enter password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label="Please confirm password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class AddTeacherForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control'}
        ),
        required=False
    )

    room_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "subject_checkboxs"}
        ))

    def clean_subjects(self):
        subjects = self.cleaned_data['subjects']
        if len(subjects) > 5:
            raise forms.ValidationError(
                "A teacher cannot take more than 5 subjects."
            )
        return subjects

    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "image", "email", "phone_number", "room_number", "subjects"]


class AddSubjectForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Subject
        fields = ['name']
