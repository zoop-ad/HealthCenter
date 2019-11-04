from django.shortcuts import render,redirect
# Create your views here.

def index(request):
    print()
    return render(request, 'healthcenter/welcome.html')

def dashboard(request):
    if request.user.is_authenticated == True:
        return render(request,'healthcenter/dashboard.html')
    else:
        return redirect('/hc')

# def signin(request):
#     print(request.POST['username'])
#     print(request.POST['password'])
#     return render(request, 'healthcenter/signin.html')