from django import forms
from .models import UserProfile
from schools.models import School

GENDER_CHOICES =(
    ('male', 'Male'), 
    ('female', 'Female'), 
    ('other', 'Other')
)

class UserProfileForm(forms.ModelForm):
    email = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class':"form-control-lg",'placeholder':"Enter your email"}), label=False)
    birthdate = forms.DateField(label='birthdate', widget=forms.DateInput(
        attrs={'class':"form-control-lg",'type':"date",'placeholder':"Select your birthdate"}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select(
        attrs={'class':"form-control-lg", 'placeholder':"Select Gender"}))
    school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label="Select Your School",
                                    widget=forms.Select(attrs={'placeholder':"Select School"}))
    
    class Meta:
        model = UserProfile
        fields = ['email','birthdate','gender','school']