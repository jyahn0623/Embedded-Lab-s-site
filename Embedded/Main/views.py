from django.shortcuts import render
from django.views.generic import View
# Create your views here.

class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Main/index.html', {})

def ViewMembers(request):
    return render(request, 'Main/Introduction_members.html', {})
