from django.shortcuts import render ,redirect
# Create your views here.
def index(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def test_branch(request):
    return render(request,'test_branch.html')