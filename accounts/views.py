from django.shortcuts import render ,redirect
# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def ksr(request):
    return render(request,"sriram.html")

def demo(request):
    return render(request,'demo.html')