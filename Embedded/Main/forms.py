from django import forms
from Main.models import *
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['p_user',]
        widgets  = {'p_grade' : forms.Select(choices=[('1', '1'), \
            ('2', '2'), ('3', '3'), ('4', '4')])}
    
  
class RegisterForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {'password' : forms.PasswordInput(), }
    
        