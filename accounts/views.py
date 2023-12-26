from django.shortcuts import render ,redirect
# Create your views here.
def home(request):
    return render(request,'home.html')

def admin_base(request):
    try:
        return render(request,'admin_base.html')
    except:
        return render(request,'error-404.html')

def client_login(request):
    return render(request,'client_login.html')

def service(request):
    return render(request,'service.html')

def home2(request):
    return render(request,'home.html')

# def login(request):
#     return render(request,'login.html')

