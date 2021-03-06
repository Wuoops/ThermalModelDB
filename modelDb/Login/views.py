from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

def login_view(request):

    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next')
            if next != None:
                return redirect(next)
            else:
                return redirect('/homepage/')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

@login_required
def logoutfunction(request):
    logout(request)
    return redirect('/materials')
