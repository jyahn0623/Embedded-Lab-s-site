from django import forms
from Main.models import *
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import re
def name_validator(name):
    regex = re.compile(r'^[가-힣]{2,4}$')
    if regex.search(name):
        print("오케이")

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['p_user']
        widgets  = {'p_grade' : forms.Select(choices=[('1', '1'), \
            ('2', '2'), ('3', '3'), ('4', '4')]),
            'p_birth_date' : forms.TextInput(attrs={'placeholder' : 'YYYY-MM-dd'})
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['p_picture'].required = False


# 1:1 중 Profile에 대해 만듦
class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['p_user',]
        widgets  = {'p_grade' : forms.Select(choices=[('1', '1'), \
            ('2', '2'), ('3', '3'), ('4', '4')]),
            'p_birth_date' : forms.TextInput(attrs={'placeholder' : 'YYYY-MM-dd'})
        }

    def __init__(self, *args, **kwargs):
        context = super(EditProfile, self).__init__(*args, **kwargs)
        self.fields['p_picture'].required = False
        return context
    

class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
  
class RegisterForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password' : forms.PasswordInput(),
              }
        labels = {'username' : '아이디', 'email' : '이메일'}
        help_texts = {'username' : '150이하 문자 입력해 주세요.', }

class BoardForm(forms.ModelForm):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Board
        exclude = ['b_user', ]
        widgets = {
            'b_content': SummernoteWidget(attrs={'summernote' : \
                    {'lang' : 'ko-KR', 'width' : '100%'},   
                }),
            'b_title' : forms.TextInput(attrs={"size" : "100%"})
        }
        
    
