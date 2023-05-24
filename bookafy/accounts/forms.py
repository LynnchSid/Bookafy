from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm ,UserChangeForm
from django.contrib.auth import login, authenticate
from django.db import transaction
from accounts.models import User
from userprofiles.models import UserProfile
from schools.models import School
from django.forms import ModelForm ,Textarea, TextInput, EmailInput, PasswordInput, FileInput 
from crispy_forms.helper import FormHelper
from django.db.models import Q


  
class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=100, label="first_name", widget=forms.TextInput(
        attrs={'class':"form-control-lg",'placeholder':"First Name"}))
    last_name = forms.CharField(max_length=100, label="last_name", widget=forms.TextInput(
        attrs={'class':"form-control-lg",'placeholder':"Last Name"}))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class':"form-control-lg",'placeholder':"Enter your mobile number" }))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class':"form-control-lg",'placeholder':"Enter your email address" }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class':"form-control-lg",'placeholder':"****************"})) 
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs = {'class':"form-control-lg",'placeholder':"****************"}))

    class Meta:
        model = User
        fields = ['phone', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

 

class LoginForm(forms.Form):
    username_or_email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':"Enter your Email/Phone number" }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {'placeholder':"Password"}))

    def clean_phone(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        if not  User.objects.filter(Q(phone__iexact=self.cleaned_data['username_or_email']) | Q(email__iexact=self.cleaned_data['username_or_email'])):
            raise forms.ValidationError('Email/Phone number does not exists.')
        return username_or_email

    def clean_password(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')   
 
        if username_or_email and password:
            phone_qs = User.objects.filter(Q(phone__iexact=self.cleaned_data['username_or_email']) | Q(email__iexact=self.cleaned_data['username_or_email']))
            if not phone_qs.exists():
                raise forms.ValidationError("The user does not exist")
            else:
                user = authenticate(username=username_or_email, password=password)
                if not user:
                    raise forms.ValidationError("Incorrect password. Please try again!")                    
        return password


    # def clean(self):
    #     try:
    #         phone = User.objects.get(phone__iexact=self.cleaned_data['phone'])
    #     except:
    #         raise forms.ValidationError("We cannot find an account with that mobile number.")
    #     password = self.cleaned_data['password']

    #     user = authenticate(phone=phone, password=password)
    #     if user is None:
    #         raise forms.ValidationError("Your password is incorrect.")
            
    #     return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
        }


class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



 
 

