from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.views.generic import View, ListView, FormView
from django.views.generic.edit import UpdateView, DeleteView
from Main.forms import *
from Main.models import *
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, inlineformset_factory
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
        print(request.GET.get("next"))
        return render(request, 'Main/login.html', {'next' : request.GET.get('next')})

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

        return redirect(request.GET.get('next', '/'))

@login_required        
def mypage(request):
    return render(request, "Main/mypage.html", {})

@login_required
def editUser(request):
    if request.method == 'POST':
        f1 = EditProfile(request.POST, request.FILES, instance=Profile.objects.get(p_user=request.user))
        f2 = EditUser(request.POST, request.FILES, instance=request.user)

        if f1.is_valid() and f2.is_valid():
            f2.save()
            f1.p_user = f2
            f1.save()
            return redirect('/mypage/')   
    else:
        f1 = EditProfile(instance=Profile.objects.get(p_user=request.user))
        f2 = EditUser(instance=request.user)
    return render(request, "Main/user_edit.html", {
        "f1" : f1, "f2" : f2})

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

def file_save_handler(filedatas, instance):
    for f in filedatas:
        BoardFiles.objects.create(
            b_board= instance,
            b_file = f
        )

class WriteBoard(LoginRequireMixin, FormView):
    form_class = BoardForm
    template_name = "Main/board_write.html"
    success_url = "/board/"

    def form_valid(self, form):
        form.instance.b_user = self.request.user
        form.save()
        if self.request.FILES.getlist('files'):
            file_save_handler(self.request.FILES.getlist('files'), form.instance)
        return super(WriteBoard, self).form_valid(form)
        
class EditBoard(UpdateView):
    model = Board
    form_class = BoardForm
    template_name = 'Main/board_edit.html'
    success_url = '/board/'

    def form_valid(self, form):
        boardfiles = form.instance.boardfiles_set.all()
        if self.request.FILES.getlist('files'):
            file_save_handler(self.request.FILES.getlist('files'), form.instance)
        return super(EditBoard, self).form_valid(form)

    def get_initial(self):
        board = self.get_object() # get_object()를 통하여 해당 폼의 대상 객체 추출 가능
        print(board.boardfiles_set.all()) # 보안상 파일은 inital이 안 된다고 함.
        return { 'b_files' :  board.boardfiles_set.all() }
    
    # 그럼, 콘텍스트로 URL을 보내 삭제할 수 있도록 해보자.
    def get_context_data(self, **kwargs):
        context = super(EditBoard, self).get_context_data(**kwargs)
        context['o_files'] = self.get_object().boardfiles_set.all()
        return context

def delFileWithAjax(request, pk):
    if request.method == 'POST':
        try:
            a = BoardFiles.objects.get(id=pk)
            a.delete()
            msg = "삭제가 완료 되었습니다."
        except Exception:
            msg = "삭제 도중 오류가 발생했습니다."
        context = {"msg" : msg,}
        return HttpResponse(json.dumps(context), content_type="application/json")

def DeleteBoard(request, b_pk):
    Board.objects.get(id=b_pk).delete()
    return redirect('/board/')

def searchBoard(request):
    page_ = request.GET.get("page", None)
    keyword = request.GET.get("keyword")
    notice_board = Board.objects.filter(b_isNotice=True)[:5]
    res = Board.objects.filter(Q(b_title__icontains=keyword)|Q(b_user__username=keyword), b_isNotice=False)
    p = Paginator(res, 10)
    # 키워드 검색 후 페이지네이션에 따른 보여줄 리스트
    if page_:
        viewing_list = p.page(page_).object_list
        paginator_obj = p.page(page_)
    else:
        viewing_list = p.page(1).object_list
        paginator_obj = p.page(1)
    return render(request, "Main/board.html", {
        "boards" : viewing_list, 'p' : paginator_obj,
        'keyword' : keyword,
        "notice" : notice_board
        })

class ViewBoard(ListView):
    template_name = 'Main/board.html'
    context_object_name = 'boards'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["notice"] = Board.objects.filter(b_isNotice=True)[:5]
        return data

    def get_queryset(self):
        return Board.objects.filter(b_isNotice=False).order_by('-b_date')

@login_required
def readBoard(request, b_id):
    board = Board.objects.get(id=b_id)

    return render(request, "Main/read_borad.html", {
        'board' : board,
        'files' : board.boardfiles_set.all()
    })


@login_required
def ViewMembers(request):
    return render(request, 'Main/Introduction_members.html', {})

# 아이디 중복 체크 
def isExistsID(request):
    _id = request.POST.get("id")
    s = False
    try:
        User.objects.get(username=_id)
    except Exception:
        s = True
    return HttpResponse(json.dumps({'s' : s,}), content_type="application/json")

def register(request):
    profile_form = RegisterForm()
    profile_form1 = RegisterForm1()
    
    if request.method == 'POST':
        p1 = RegisterForm(request.POST, request.FILES)
        p2 = RegisterForm1(request.POST)
         
        if p2.is_valid() and p1.is_valid():
            i = p2.save()
            j = p1.save() # form의 save의 결과는 디폴트는 instance가 반환되는 것을 활용
            j.p_user = i
            j.save(update_fields=['p_user',])
            return redirect('/')
        print(p1.errors, p2.errors)
    return render(request, 'Main/register.html', {
        'f1' : profile_form, 
        'f2' : profile_form1,
 
    })

def guestbook(request):
    obj = GuestBook.objects.all().order_by('-g_date')
    return render(request, 'Main/guestbook.html', {
        'obj' : obj[:3],
        'totalcnt' : int(obj.__len__()/3)
    })

def ajaxguestbook(request):
    msg = True
    page = int(request.POST.get('page'))
    gb= GuestBook.objects.all().order_by('-g_date')[page+3:page+6]
    gb_datas = {}
    if not gb:
        msg = False
    else:
        for item in gb:
            gb_datas[item.id] = {
                'g_name' : item.g_name,
                'g_content' : item.g_content,
                'g_title' : item.g_title,
                'g_email' : item.g_email
            }
    datas = {
        'gb' : gb_datas,
        'status' : msg
    }
    return HttpResponse(json.dumps(datas), content_type="application/json")

def guestbookWrite(request):
    from datetime import datetime
    hxff = request.META.get('HTTP_X_FORWARDED_FOR')
    if hxff:
        ip = hxff.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    datas = {
        'g_name' : request.POST.get('name'),
        'g_content' : request.POST.get('message'),
        'g_title' : request.POST.get('subject'),
        'g_email' : request.POST.get('email'),
        'g_ip' : ip
    }

    GuestBook.objects.create(
        **datas
    )

    return redirect('/guestbook/')


