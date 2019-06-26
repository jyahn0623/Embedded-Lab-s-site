from django.shortcuts import render, redirect, render_to_response
from django.views.generic import View
from Main.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# 로긴 믹스인
class LoginRequireMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequireMixin, cls).as_view(**kwargs)
        return login_required(view)

class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Main/index.html', {})

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Main/login.html', {})

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('id')
        user_pw = request.POST.get('pw')

        try:
            user = User.objects.get(username=user_id)
        except Exception:
            return render(request, 'Main/login.html', {'msg' : '잘못된 아이디입니다.', })
        
        if user.password != user_pw:
            return render(request, 'Main/login.html', {'msg' : '비밀번호가 틀립니다.', })

        login(request, user)  
        return redirect('/')

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        print('logout')
        return redirect('/')

@login_required
def ViewMembers(request):
    return render(request, 'Main/Introduction_members.html', {})

def register(request):
    profile_form = RegisterForm()
    profile_form1 = RegisterForm1()
    
    if request.method == 'POST':
        p1 = RegisterForm(request.POST)
        p2 = RegisterForm1(request.POST)
         
        if p2.is_valid() and p1.is_valid():
            i = p2.save()
            j = p1.save() # form의 save의 결과는 디폴트는 instance가 반환되는 것을 활용
            j.p_user = i
            j.save(update_fields=['p_user',])
            return redirect('/')

    return render(request, 'Main/register.html', {
        'f1' : profile_form, 
        'f2' : profile_form1
    })
